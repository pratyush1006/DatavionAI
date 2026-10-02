from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor

from django.core.cache import cache
from django.test import SimpleTestCase, override_settings

from apps.ai.services.deployment import (
    deployment_status,
    validate_deployment_environment,
)
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


class FinalProductionCertificationTests(SimpleTestCase):
    def setUp(self):
        cache.clear()

    def test_canonical_ai_domain(self):
        import apps.ai.services

        self.assertIsNotNone(apps.ai.services)

    def test_liveness(self):
        self.assertEqual(liveness()["status"], "ok")

    def test_readiness_contract(self):
        result = readiness()
        self.assertIn("database", result["checks"])
        self.assertIn("redis", result["checks"])

    def test_distributed_circuit(self):
        cfg = DistributedCircuitConfig(failure_threshold=2, recovery_seconds=60)
        record_failure("cert-provider", config=cfg)
        self.assertFalse(is_open("cert-provider", config=cfg))
        record_failure("cert-provider", config=cfg)
        self.assertTrue(is_open("cert-provider", config=cfg))
        record_success("cert-provider", config=cfg)
        self.assertFalse(is_open("cert-provider", config=cfg))

    def test_open_circuit_blocks_call(self):
        cfg = DistributedCircuitConfig(failure_threshold=1, recovery_seconds=60)
        record_failure("cert-provider", config=cfg)
        with self.assertRaises(DistributedCircuitOpenError):
            call_with_distributed_circuit(
                "cert-provider",
                lambda: (_ for _ in ()).throw(AssertionError("must not run")),
                config=cfg,
            )

    @override_settings(AI_PROVIDER_TIMEOUT_SECONDS=15, AI_PROVIDER_RETRY_COUNT=2)
    def test_provider_timeout_contract(self):
        cfg = provider_http_config()
        self.assertGreaterEqual(cfg.total_timeout, 0.1)
        self.assertLessEqual(cfg.connect_timeout, cfg.total_timeout)
        self.assertLessEqual(cfg.read_timeout, cfg.total_timeout)
        self.assertEqual(cfg.retries, 2)

    def test_concurrent_runtime_contract(self):
        def call():
            time.sleep(0.005)

        result = benchmark_concurrent(call, concurrency=4, iterations=12)
        self.assertEqual(result.count, 12)
        self.assertEqual(result.failures, 0)
        self.assertGreater(result.throughput_per_second, 0)

    def test_cache_concurrency(self):
        def operation(index):
            key = f"datavion:ai:cert:{index}"
            cache.set(key, "ok", timeout=20)
            return cache.get(key)

        with ThreadPoolExecutor(max_workers=8) as executor:
            values = list(executor.map(operation, range(16)))

        self.assertEqual(values, ["ok"] * 16)

    def test_deployment_validator_fail_closed(self):
        with override_settings(
            DEBUG=True,
            SECRET_KEY="test-secret",
            ALLOWED_HOSTS=["*"],
            REDIS_URL="",
            AI_PROVIDER="",
            SESSION_COOKIE_SECURE=False,
            CSRF_COOKIE_SECURE=False,
        ):
            self.assertTrue(validate_deployment_environment(production=True))

    @override_settings(
        DEBUG=False,
        SECRET_KEY="production-certification-secret",
        ALLOWED_HOSTS=["api.example.com"],
        REDIS_URL="redis://localhost:6379/0",
        AI_PROVIDER="openai",
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
    )
    def test_production_security_contract(self):
        status = deployment_status()
        self.assertFalse(status.debug)
        self.assertTrue(status.secret_key_configured)
        self.assertTrue(status.allowed_hosts_configured)
        self.assertTrue(status.redis_configured)
        self.assertTrue(status.provider_configured)
        self.assertTrue(status.secure_cookies)

    def test_no_provider_secret_is_written_by_certification(self):
        self.assertNotIn("OPENAI_API_KEY", os.environ)
