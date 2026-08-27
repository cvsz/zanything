"""Secret Management provider interface and redactor."""

import os
import re
from abc import ABC, abstractmethod
from typing import ClassVar

from zanything.logging import get_logger

logger = get_logger("zanything.secrets")


class SecretProvider(ABC):
    """Abstract interface for secret resolution (Environment/Vault)."""

    @abstractmethod
    def get_secret(self, secret_ref: str) -> str | None:
        """Resolve a secret value by its reference URI or name."""
        pass


class EnvSecretProvider(SecretProvider):
    """Resolves secret references from environment variables."""

    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix

    def get_secret(self, secret_ref: str) -> str | None:
        # e.g., "env://OPENAI_API_KEY" or "OPENAI_API_KEY"
        clean_name = secret_ref.removeprefix("env://")
        env_key = f"{self.prefix}{clean_name}"
        return os.environ.get(env_key)


class SecretRedactor:
    """Utility to mask credentials and sensitive patterns in logs."""

    SECRET_PATTERNS: ClassVar[list[re.Pattern[str]]] = [
        re.compile(r"(bearer\s+)[a-zA-Z0-9\._\-]+", re.IGNORECASE),
        re.compile(r"(api[_\-]?key\s*[:=]\s*)[a-zA-Z0-9\._\-]+", re.IGNORECASE),
        re.compile(r"(password\s*[:=]\s*)[^\s,]+", re.IGNORECASE),
        re.compile(r"(ghp_[a-zA-Z0-9]{36})", re.IGNORECASE),
        re.compile(r"(xoxb-[a-zA-Z0-9\-]+)", re.IGNORECASE),
    ]

    @classmethod
    def redact(cls, text: str) -> str:
        """Redact known secret patterns from string."""
        redacted = text
        for pattern in cls.SECRET_PATTERNS:
            redacted = pattern.sub(r"\1[REDACTED]", redacted)
        return redacted
