"""Artifact storage abstraction and metadata tracking with checksums and provenance."""

import hashlib
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field

from zanything.logging import get_logger

logger = get_logger("zanything.artifacts")


class ArtifactMetadata(BaseModel):
    """Immutable metadata describing stored artifact."""

    artifact_id: str
    tenant_id: str
    filename: str
    content_type: str
    size_bytes: int
    sha256: str
    provenance_task_id: str
    storage_path: str
    extra: dict[str, Any] = Field(default_factory=dict)


class ArtifactStorage(ABC):
    """Abstract object storage interface for build artifacts and reports."""

    @abstractmethod
    async def store(
        self,
        tenant_id: str,
        filename: str,
        content: bytes,
        content_type: str,
        task_id: str,
    ) -> ArtifactMetadata:
        """Store artifact content and return metadata with SHA256 checksum."""
        pass

    @abstractmethod
    async def retrieve(self, tenant_id: str, artifact_id: str) -> bytes | None:
        """Retrieve artifact binary content enforcing tenant boundary."""
        pass

    @abstractmethod
    async def get_metadata(
        self, tenant_id: str, artifact_id: str
    ) -> ArtifactMetadata | None:
        """Get artifact metadata."""
        pass


class MemoryArtifactStorage(ArtifactStorage):
    """In-memory reference artifact storage with strict tenant isolation."""

    def __init__(self) -> None:
        self._storage: dict[str, bytes] = {}
        self._meta: dict[str, ArtifactMetadata] = {}

    async def store(
        self,
        tenant_id: str,
        filename: str,
        content: bytes,
        content_type: str,
        task_id: str,
    ) -> ArtifactMetadata:
        sha256 = hashlib.sha256(content).hexdigest()
        artifact_id = f"art-{sha256[:16]}"
        storage_key = f"{tenant_id}/{artifact_id}"

        meta = ArtifactMetadata(
            artifact_id=artifact_id,
            tenant_id=tenant_id,
            filename=filename,
            content_type=content_type,
            size_bytes=len(content),
            sha256=sha256,
            provenance_task_id=task_id,
            storage_path=storage_key,
        )

        self._storage[storage_key] = content
        self._meta[storage_key] = meta
        logger.info(
            f"Stored artifact '{filename}' ({len(content)} bytes) "
            f"for tenant '{tenant_id}' [SHA256: {sha256[:8]}]"
        )
        return meta

    async def retrieve(self, tenant_id: str, artifact_id: str) -> bytes | None:
        storage_key = f"{tenant_id}/{artifact_id}"
        return self._storage.get(storage_key)

    async def get_metadata(
        self, tenant_id: str, artifact_id: str
    ) -> ArtifactMetadata | None:
        storage_key = f"{tenant_id}/{artifact_id}"
        return self._meta.get(storage_key)
