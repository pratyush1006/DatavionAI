"""
Package-level tests for the DatavionOS kernel.
"""

from __future__ import annotations

from django.apps import apps

from apps.datavionos import __version__
from apps.datavionos.constants import (
    DATAVIONOS_CODENAME,
    DATAVIONOS_NAME,
    DATAVIONOS_VENDOR,
    DATAVIONOS_VERSION,
    VERSION,
)
from apps.datavionos.contracts import (
    BaseContract,
    ContractMetadata,
)
from apps.datavionos.exceptions import (
    CapabilityError,
    CompositionError,
    ConfigurationError,
    ContractError,
    DatavionOSError,
    EventError,
    KernelError,
    PluginError,
    RegistryError,
    RuntimeError,
    ValidationError,
    WorkflowError,
)
from apps.datavionos.types import (
    CapabilityName,
    Context,
    FeatureFlag,
    Identifier,
    Labels,
    Metadata,
    PermissionName,
    PluginName,
    Properties,
    TagSet,
    TenantIdentifier,
    UserIdentifier,
    WorkspaceIdentifier,
)


def test_version_matches_package() -> None:
    """
    The package version should expose the canonical version constant.
    """
    assert __version__ == DATAVIONOS_VERSION
    assert VERSION == DATAVIONOS_VERSION


def test_product_metadata() -> None:
    """
    Verify product metadata constants.
    """
    assert DATAVIONOS_NAME == "DatavionOS"
    assert DATAVIONOS_VENDOR == "DatavionAI"
    assert DATAVIONOS_CODENAME == "Genesis"


def test_django_app_configuration() -> None:
    """
    Verify the Django application is registered correctly.
    """
    config = apps.get_app_config("datavionos")

    assert config.name == "apps.datavionos"
    assert config.label == "datavionos"
    assert config.verbose_name == "DatavionOS"


def test_base_contract() -> None:
    """
    BaseContract should provide common metadata.
    """

    class SampleContract(BaseContract):
        pass

    contract = SampleContract()

    assert contract.contract_name() == "SampleContract"
    assert contract.contract_version() == 1
    assert contract.schema.endswith(":v1")
    assert contract.to_dict() == {}


def test_contract_metadata_factory() -> None:
    """
    Metadata factory should populate required fields.
    """

    class SampleContract(BaseContract):
        pass

    metadata = ContractMetadata.create(
        contract=SampleContract,
        source="unit-test",
    )

    assert metadata.contract == "SampleContract"
    assert metadata.version == 1
    assert metadata.source == "unit-test"
    assert metadata.identifier
    assert metadata.namespace.endswith("SampleContract")
    assert metadata.is_version_supported


def test_exception_hierarchy() -> None:
    """
    All kernel exceptions should inherit from DatavionOSError.
    """
    exception_types = (
        ConfigurationError,
        ValidationError,
        ContractError,
        RuntimeError,
        KernelError,
        RegistryError,
        PluginError,
        CapabilityError,
        CompositionError,
        WorkflowError,
        EventError,
    )

    for exception_type in exception_types:
        exception = exception_type(message="test")

        assert isinstance(exception, DatavionOSError)
        assert str(exception)
        assert exception.to_dict()["message"] == "test"


def test_type_aliases() -> None:
    """
    Verify exported typing aliases are usable.
    """
    identifier: Identifier = Identifier("id")
    tenant: TenantIdentifier = TenantIdentifier("tenant")
    workspace: WorkspaceIdentifier = WorkspaceIdentifier("workspace")
    user: UserIdentifier = UserIdentifier("user")
    plugin: PluginName = PluginName("patients")
    capability: CapabilityName = CapabilityName("patients.read")
    permission: PermissionName = PermissionName("patients.view")
    feature: FeatureFlag = FeatureFlag("ai.enabled")

    metadata: Metadata = {}
    context: Context = {}
    properties: Properties = {}
    labels: Labels = {}
    tags: TagSet = {"core"}

    assert str(identifier) == "id"
    assert str(tenant) == "tenant"
    assert str(workspace) == "workspace"
    assert str(user) == "user"
    assert str(plugin) == "patients"
    assert str(capability) == "patients.read"
    assert str(permission) == "patients.view"
    assert str(feature) == "ai.enabled"

    assert metadata == {}
    assert context == {}
    assert properties == {}
    assert labels == {}
    assert tags == {"core"}
