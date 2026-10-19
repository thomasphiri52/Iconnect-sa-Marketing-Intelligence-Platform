from __future__ import annotations

import csv
import hashlib
import json
import os
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DEFAULT_DB = DATA_DIR / "iconnect_enterprise.db"

SCHEMA = '''
CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    tenant_id INTEGER,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
);

CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT NOT NULL,
    resource TEXT,
    details TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS data_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    source_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'configured',
    last_run TEXT,
    row_count INTEGER NOT NULL DEFAULT 0,
    quality_score REAL NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id INTEGER NOT NULL,
    filename TEXT,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    status TEXT NOT NULL,
    rows_loaded INTEGER NOT NULL DEFAULT 0,
    rows_rejected INTEGER NOT NULL DEFAULT 0,
    error TEXT,
    checksum TEXT,
    FOREIGN KEY (source_id) REFERENCES data_sources(id)
);

CREATE TABLE IF NOT EXISTS market_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_date TEXT NOT NULL,
    province TEXT NOT NULL,
    category TEXT NOT NULL,
    demand REAL,
    growth REAL,
    revenue REAL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS competitor_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_date TEXT NOT NULL,
    competitor TEXT NOT NULL,
    activity REAL,
    pricing_index REAL,
    campaign_count INTEGER,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    province TEXT,
    category TEXT,
    score REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    owner TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    severity TEXT NOT NULL,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    owner TEXT,
    priority TEXT NOT NULL DEFAULT 'medium',
    status TEXT NOT NULL DEFAULT 'open',
    due_date TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    report_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'generated',
    created_at TEXT NOT NULL,
    payload TEXT
);
'''

@dataclass
class IngestionResult:
    source: str
    status: str
    rows_loaded: int
    rows_rejected: int
    quality_score: float
    error: str = ""

def now():
    return datetime.now(timezone.utc).isoformat()

def get_db_path():
    return Path(os.getenv("ICONNECT_DB_PATH", str(DEFAULT_DB)))

def connect():
    path = get_db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def initialize():
    with connect() as conn:
        conn.executescript(SCHEMA)
        conn.execute(
            "INSERT OR IGNORE INTO tenants(name, status, created_at) VALUES (?, ?, ?)",
            ("iConnect SA Demo Tenant", "active", now())
        )
        conn.commit()

def health():
    initialize()
    with connect() as conn:
        conn.execute("SELECT 1").fetchone()
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchall()
        counts = {}
        for row in tables:
            name = row["name"]
            counts[name] = conn.execute(f"SELECT COUNT(*) AS c FROM {name}").fetchone()["c"]
    size = get_db_path().stat().st_size if get_db_path().exists() else 0
    return {"status": "healthy", "path": str(get_db_path()), "size_bytes": size, "tables": counts}

def register_source(name, source_type):
    initialize()
    with connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO data_sources(name, source_type, created_at) VALUES (?, ?, ?)",
            (name, source_type, now())
        )
        conn.commit()

def ingest_csv(path, source_name=None):
    initialize()
    path = Path(path)
    source_name = source_name or path.stem
    register_source(source_name, "CSV")
    checksum = hashlib.sha256(path.read_bytes()).hexdigest()
    started = now()
    loaded = rejected = 0
    error = ""
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("CSV has no header row")
            rows = list(reader)

        with connect() as conn:
            source_id = conn.execute(
                "SELECT id FROM data_sources WHERE name=?", (source_name,)
            ).fetchone()["id"]
            for row in rows:
                try:
                    # Flexible landing-zone storage in audit_events keeps ingestion
                    # useful without forcing a business-specific schema.
                    conn.execute(
                        "INSERT INTO audit_events(username, action, resource, details, created_at) "
                        "VALUES (?, ?, ?, ?, ?)",
                        ("system", "DATA_INGEST", source_name, json.dumps(row), now())
                    )
                    loaded += 1
                except Exception:
                    rejected += 1
            total = loaded + rejected
            quality = round((loaded / total) * 100, 1) if total else 0.0
            conn.execute(
                "UPDATE data_sources SET status=?, last_run=?, row_count=?, quality_score=? WHERE id=?",
                ("healthy" if rejected == 0 else "warning", now(), loaded, quality, source_id)
            )
            conn.execute(
                "INSERT INTO ingestion_runs(source_id, filename, started_at, completed_at, status, "
                "rows_loaded, rows_rejected, checksum) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (source_id, path.name, started, now(),
                 "completed" if rejected == 0 else "completed_with_warnings",
                 loaded, rejected, checksum)
            )
            conn.commit()
        return IngestionResult(source_name, "completed", loaded, rejected, quality)
    except Exception as exc:
        error = str(exc)
        with connect() as conn:
            source_id = conn.execute(
                "SELECT id FROM data_sources WHERE name=?", (source_name,)
            ).fetchone()["id"]
            conn.execute(
                "INSERT INTO ingestion_runs(source_id, filename, started_at, completed_at, status, error, checksum) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (source_id, path.name, started, now(), "failed", error, checksum)
            )
            conn.commit()
        return IngestionResult(source_name, "failed", loaded, rejected, 0.0, error)

def seed_demo():
    initialize()
    with connect() as conn:
        existing = conn.execute("SELECT COUNT(*) AS c FROM market_metrics").fetchone()["c"]
        if existing:
            return False
        provinces = ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape"]
        for i, province in enumerate(provinces):
            conn.execute(
                "INSERT INTO market_metrics(metric_date, province, category, demand, growth, revenue, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (datetime.now().date().isoformat(), province, "Business Services",
                 70 + i*5, 6.5 + i*1.4, 1200000 + i*250000, now())
            )
        for name, activity in [("Competitor A", 78), ("Competitor B", 61), ("Competitor C", 46)]:
            conn.execute(
                "INSERT INTO competitor_metrics(metric_date, competitor, activity, pricing_index, campaign_count, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (datetime.now().date().isoformat(), name, activity, 95+i if 'i' in locals() else 100, 4+i if 'i' in locals() else 4, now())
            )
        conn.execute(
            "INSERT INTO opportunities(title, province, category, score, status, owner, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("Gauteng Expansion Opportunity", "Gauteng", "Business Services", 91, "open", "Executive", now())
        )
        conn.execute(
            "INSERT INTO alerts(severity, title, message, status, created_at) VALUES (?, ?, ?, ?, ?)",
            ("high", "Competitor activity elevated", "Competitor A activity is above the configured monitoring threshold.", "open", now())
        )
        conn.commit()
        return True

def recent_ingestions(limit=10):
    initialize()
    with connect() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT ir.*, ds.name AS source_name FROM ingestion_runs ir "
            "JOIN data_sources ds ON ds.id=ir.source_id ORDER BY ir.id DESC LIMIT ?", (limit,)
        ).fetchall()]

def source_rows():
    initialize()
    with connect() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM data_sources ORDER BY name"
        ).fetchall()]

def table_counts():
    return health()["tables"]
