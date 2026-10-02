from __future__ import annotations

import time
from unittest.mock import patch

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings

from apps.ai.services.deployment import deployment_status
from apps.ai.services.distributed_circuit import (
    DistributedCircuitConfig,
    DistributedCircuitOpenError,
    call_with_distributed_circuit,
    is_open,
    record_failure,
    record_success,
)
from apps.ai.services.health import liveness, readiness
from apps.ai.services.performance import benchmark_concurrent
from apps.ai.services.provider_http import provider_http_config


class DistributedCircuitTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def test_failure_threshold_is_shared_via_cache(self):
        config = DistributedCircuitConfig(failure_threshold=2, recovery_seconds=60)
        record_failure("test-provider", config=config)
        self.assertFalse(is_open("test-provider", config=config))
        record_failure("test-provider", config=config)
        self.assertTrue(is_open("test-provider", config=config))
        record_success("test-provider", config=config)
        self.assertFalse(is_open("test-provider", config=config))

    def test_open_circuit_blocks_call(self):
        config = DistributedCircuitConfig(failure_threshold=1, recovery_seconds=60)
        record_failure("test-provider", config=config)
        with self.assertRaises(DistributedCircuitOpenError):
            call_with_distributed_circuit(
                "test-provider",
                lambda: "should-not-run",
                config=config,
            )

    def test_recovery_window_closes_circuit(self):
        config = DistributedCircuitConfig(failure_threshold=1, recovery_seconds=1)
        record_failure("test-provider", config=config)
        self.assertTrue(is_open("test-provider", config=config))
        with patch(
            "apps.ai.services.distributed_circuit.time.time",
            return_value=time.time() + 2,
        ):
            self.assertFalse(is_open("test-provider", config=config))


class ProviderHTTPTests(SimpleTestCase):
    @override_settings(
        AI_PROVIDER_TIMEOUT_SECONDS=12,
        AI_PROVIDER_RETRY_COUNT=3,
    )
    def test_provider_timeout_and_retry_are_bounded(self):
        config = provider_http_config()
        self.assertEqual(config.total_timeout, 12.0)
        self.assertEqual(config.retries, 3)
        self.assertLessEqual(config.connect_timeout, config.total_timeout)
        self.assertLessEqual(config.read_timeout, config.total_timeout)


class PerformanceTests(SimpleTestCase):
    def test_concurrent_benchmark_runs(self):
        def call():
            time.sleep(0.01)

        summary = benchmark_concurrent(call, concurrency=4, iterations=8)
        self.assertEqual(summary.count, 8)
        self.assertEqual(summary.failures, 0)
        self.assertGreater(summary.throughput_per_second, 0)


class HealthTests(SimpleTestCase):
    def test_liveness_is_independent_of_dependencies(self):
        self.assertEqual(liveness()["status"], "ok")

    def test_readiness_reports_dependencies(self):
        result = readiness()
        self.assertIn(result["status"], {"ok", "degraded"})
        self.assertIn("database", result["checks"])
        self.assertIn("redis", result["checks"])


class DeploymentTests(SimpleTestCase):
    @override_settings(
        DEBUG=False,
        SECRET_KEY="production-test-secret",
        ALLOWED_HOSTS=["api.example.com"],
        REDIS_URL="redis://localhost:6379/0",
        AI_PROVIDER="openai",
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
    )
    def test_production_status_contract(self):
        status = deployment_status()
        self.assertFalse(status.debug)
        self.assertTrue(status.secret_key_configured)
        self.assertTrue(status.allowed_hosts_configured)
        self.assertTrue(status.redis_configured)
        self.assertTrue(status.provider_configured)
        self.assertTrue(status.secure_cookies)
