from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

try:
    from enterprise_data_platform import connect, initialize, now
except ImportError:
    connect = None
    def now():
        return datetime.now(timezone.utc).isoformat()
    def initialize():
        return None

API_VERSION = "v1"
WEBHOOK_EVENTS = {
    "market.signal",
    "competitor.alert",
    "opportunity.created",
    "data.ingestion.completed",
    "executive.brief.ready",
}

@dataclass
class APIKey:
    key_id: str
    key_hash: str
    label: str
    active: bool = True
    created_at: str = ""

@dataclass
class ConnectorStatus:
    name: str
    connector_type: str
    status: str
    last_sync: str
    records: int
    message: str = ""

def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def create_api_key(label: str = "iConnect Integration"):
    raw = "icsa_" + secrets.token_urlsafe(30)
    key = APIKey(
        key_id="key_" + secrets.token_hex(8),
        key_hash=_hash(raw),
        label=label,
        created_at=now(),
    )
    return raw, key

def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    return hmac.compare_digest(_hash(raw_key), stored_hash)

def api_catalog():
    return [
        {"method": "GET", "path": f"/api/{API_VERSION}/health", "purpose": "Platform health"},
        {"method": "GET", "path": f"/api/{API_VERSION}/market", "purpose": "Market intelligence"},
        {"method": "GET", "path": f"/api/{API_VERSION}/competitors", "purpose": "Competitor signals"},
        {"method": "GET", "path": f"/api/{API_VERSION}/opportunities", "purpose": "Opportunity radar"},
        {"method": "GET", "path": f"/api/{API_VERSION}/alerts", "purpose": "Risk and alert feed"},
        {"method": "POST", "path": f"/api/{API_VERSION}/ingest", "purpose": "Data ingestion"},
        {"method": "POST", "path": f"/api/{API_VERSION}/webhooks/test", "purpose": "Webhook delivery test"},
    ]

def platform_health():
    try:
        initialize()
        with connect() as conn:
            conn.execute("SELECT 1").fetchone()
        return {"status": "healthy", "api_version": API_VERSION, "timestamp": now()}
    except Exception as exc:
        return {"status": "degraded", "api_version": API_VERSION, "timestamp": now(), "error": str(exc)}

def connector_catalog():
    return [
        ConnectorStatus("CSV / Excel", "file", "ready", now(), 0, "Manual ingestion endpoint"),
        ConnectorStatus("CRM", "rest", "configured", "—", 0, "Connector contract ready"),
        ConnectorStatus("Google Analytics", "analytics", "configured", "—", 0, "Connector contract ready"),
        ConnectorStatus("Meta Ads", "marketing", "configured", "—", 0, "Connector contract ready"),
        ConnectorStatus("Google Ads", "marketing", "configured", "—", 0, "Connector contract ready"),
        ConnectorStatus("SQL Database", "database", "configured", "—", 0, "Connector contract ready"),
        ConnectorStatus("REST API", "api", "ready", now(), 0, "Native API layer"),
    ]

def connector_payloads():
    return [
        {"connector": "CRM", "endpoint": "/api/v1/ingest", "mapping": ["customer_id", "segment", "status", "value"]},
        {"connector": "Google Analytics", "endpoint": "/api/v1/ingest", "mapping": ["date", "sessions", "conversions", "revenue"]},
        {"connector": "Meta Ads", "endpoint": "/api/v1/ingest", "mapping": ["campaign", "spend", "reach", "clicks", "conversions"]},
        {"connector": "Google Ads", "endpoint": "/api/v1/ingest", "mapping": ["campaign", "spend", "impressions", "clicks", "conversions"]},
    ]

def webhook_event(event: str, payload: Dict[str, Any]):
    if event not in WEBHOOK_EVENTS:
        raise ValueError(f"Unsupported event: {event}")
    return {
        "event": event,
        "id": "evt_" + secrets.token_hex(10),
        "created_at": now(),
        "payload": payload,
        "delivery_status": "queued",
    }
