"""
PROJECT OMNIA NEXUS: Authentication, RBAC & Multi-Tenant Isolation
Enforces strict tenant boundaries, cryptographic API key hashing, and capability permissions.
"""
from __future__ import annotations
import hashlib
import hmac
import secrets
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Set

class Role(str, Enum):
    VIEWER = "viewer"
    OPERATOR = "operator"
    FOUNDER = "founder"
    SYSTEM = "system"

ROLE_PERMISSIONS: dict[Role, Set[str]] = {
    Role.VIEWER: {"report:read", "tasks:read", "studios:read", "audit:verify"},
    Role.OPERATOR: {"report:read", "tasks:read", "tasks:write", "studios:read", "audit:verify", "evidence:write"},
    Role.FOUNDER: {"report:read", "tasks:read", "tasks:write", "studios:read", "studios:write", "audit:verify", "evidence:write", "approval:decide", "admin:all"},
    Role.SYSTEM: {"*"}
}

@dataclass
class TenantContext:
    tenant_id: str
    user_id: str
    role: Role

    def has_permission(self, permission: str) -> bool:
        if self.role == Role.SYSTEM:
            return True
        allowed = ROLE_PERMISSIONS.get(self.role, set())
        return "*" in allowed or permission in allowed

    def validate_tenant_access(self, target_tenant_id: str) -> bool:
        """Strict tenant isolation: non-system users can only access their own tenant."""
        if self.role == Role.SYSTEM:
            return True
        return self.tenant_id == target_tenant_id

class AuthManager:
    @staticmethod
    def generate_api_key(prefix: str = "omnia") -> tuple[str, str]:
        """Generates a raw secret API key and its salted SHA-256 hash."""
        secret = secrets.token_urlsafe(32)
        raw_key = f"{prefix}_{secret}"
        salt = secrets.token_hex(16)
        key_hash = hashlib.sha256(f"{raw_key}:{salt}".encode("utf-8")).hexdigest()
        stored_value = f"{salt}${key_hash}"
        return raw_key, stored_value

    @staticmethod
    def verify_api_key(raw_key: str, stored_value: str) -> bool:
        try:
            salt, expected_hash = stored_value.split("$", 1)
            computed_hash = hashlib.sha256(f"{raw_key}:{salt}".encode("utf-8")).hexdigest()
            return hmac.compare_digest(computed_hash, expected_hash)
        except Exception:
            return False
