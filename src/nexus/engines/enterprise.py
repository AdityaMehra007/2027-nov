"""
ATLAS NEXUS: Mission 09 - Multi-Tenant Enterprise Governance & Compute Governor
Tenancy isolation, Role-Based Access Control (RBAC), and quota enforcement.
"""

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    RESEARCHER = "RESEARCHER"
    DEVELOPER = "DEVELOPER"
    AUDITOR = "AUDITOR"


ROLE_PERMISSIONS: Dict[UserRole, Set[str]] = {
    UserRole.ADMIN: {"*"},
    UserRole.RESEARCHER: {
        "execute_research",
        "view_knowledge_graph",
        "run_simulation",
        "verify_claim",
    },
    UserRole.DEVELOPER: {
        "scaffold_project",
        "validate_code",
        "execute_pipeline",
        "view_knowledge_graph",
    },
    UserRole.AUDITOR: {
        "view_audit_trail",
        "inspect_telemetry",
        "verify_claim",
    },
}


@dataclass
class Tenant:
    tenant_id: str
    name: str
    admin_email: str


@dataclass
class NexusUser:
    user_id: str
    tenant_id: str
    email: str
    role: UserRole


class TenantManager:
    def __init__(self) -> None:
        self._tenants: Dict[str, Tenant] = {}
        self._users: Dict[str, NexusUser] = {}

    def create_tenant(self, name: str, admin_email: str) -> Tenant:
        tenant_id = f"TEN-{uuid.uuid4().hex[:8].upper()}"
        tenant = Tenant(tenant_id=tenant_id, name=name, admin_email=admin_email)
        self._tenants[tenant_id] = tenant
        # Auto-create admin user
        self.add_user(tenant_id=tenant_id, email=admin_email, role=UserRole.ADMIN)
        return tenant

    def add_user(self, tenant_id: str, email: str, role: UserRole) -> NexusUser:
        user_id = f"USR-{uuid.uuid4().hex[:8].upper()}"
        user = NexusUser(user_id=user_id, tenant_id=tenant_id, email=email, role=role)
        self._users[user_id] = user
        return user

    def get_user(self, user_id: str) -> Optional[NexusUser]:
        return self._users.get(user_id)

    def has_permission(self, user_id: str, permission_name: str) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        perms = ROLE_PERMISSIONS.get(user.role, set())
        return "*" in perms or permission_name in perms


class ComputeGovernor:
    def __init__(self, global_token_quota: int = 1_000_000) -> None:
        self.global_token_quota = global_token_quota
        self.remaining_tokens = global_token_quota
        self.total_compute_seconds = 0.0

    def consume(self, tokens: int, compute_seconds: float = 0.0) -> bool:
        if tokens > self.remaining_tokens:
            return False
        self.remaining_tokens -= tokens
        self.total_compute_seconds += compute_seconds
        return True
