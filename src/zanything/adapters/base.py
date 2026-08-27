"""Base integration adapter contract.

Adapters implementing this interface will be used in v9 (Integration Fabric).
Currently no production adapters exist.
"""

from abc import ABC, abstractmethod
from typing import Any


class IntegrationAdapter(ABC):
    """Abstract base for all integration adapters."""

    @abstractmethod
    def validate_config(self) -> None: ...

    @abstractmethod
    def health(self) -> dict[str, Any]: ...

    @abstractmethod
    def capabilities(self) -> dict[str, Any]: ...

    @abstractmethod
    def execute(
        self, operation: str, payload: dict[str, Any], context: dict[str, Any]
    ) -> dict[str, Any]: ...

    @abstractmethod
    def audit_metadata(self) -> dict[str, Any]: ...
