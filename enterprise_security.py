
"""iConnect SA V5 Enterprise Security Layer.
Demo-safe RBAC, API key lifecycle, audit events and tenant-aware session helpers.
Replace in-memory stores with a persistent database/identity provider in production.
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from hashlib import sha256
import secrets
from typing import Dict, List

ROLES = {
    "Super Admin": {"*"},
    "Executive": {"dashboard", "market", "competitor", "customer", "reports", "ai"},
    "Analyst": {"dashboard", "market", "competitor", "customer", "reports", "ai"},
    "Marketing Manager": {"dashboard", "market", "customer", "reports", "ai"},
    "Viewer": {"dashboard", "reports"},
}

@dataclass
class User:
    username: str
    role: str
    tenant: str = "iConnect SA"
    active: bool = True

@dataclass
class AuditEvent:
    timestamp: str
    username: str
    action: str
    resource: str
    outcome: str
    tenant: str

def allowed(role: str, permission: str) -> bool:
    return permission in ROLES.get(role, set()) or "*" in ROLES.get(role, set())

def create_user(username: str, role: str, tenant: str = "iConnect SA") -> Dict:
    if role not in ROLES:
        raise ValueError("Unknown role")
    return asdict(User(username, role, tenant))

def issue_api_key(label: str) -> Dict:
    raw = "icsa_" + secrets.token_urlsafe(28)
    return {
        "label": label,
        "key_preview": raw[:10] + "••••••",
        "key_hash": sha256(raw.encode()).hexdigest(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "Active",
        "note": "Store the raw key only in a secure secret manager."
    }

def audit(username: str, action: str, resource: str, outcome: str = "Success",
          tenant: str = "iConnect SA") -> Dict:
    return asdict(AuditEvent(
        datetime.now().isoformat(timespec="seconds"),
        username, action, resource, outcome, tenant
    ))

def default_users() -> List[Dict]:
    return [
        create_user("admin", "Super Admin"),
        create_user("executive", "Executive"),
        create_user("analyst", "Analyst"),
        create_user("marketing", "Marketing Manager"),
        create_user("viewer", "Viewer"),
    ]
