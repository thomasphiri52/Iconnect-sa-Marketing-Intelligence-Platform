from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import random
from typing import List

def now():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class LiveSignal:
    timestamp: str
    region: str
    category: str
    title: str
    value: float
    severity: str
    status: str

REGIONS = ["Gauteng", "Western Cape", "KwaZulu-Natal", "Eastern Cape", "Limpopo", "Mpumalanga"]
CATEGORIES = ["Market", "Competitor", "Customer", "Revenue", "Risk"]

def generate_live_signals(count=12, seed=None) -> List[LiveSignal]:
    rng = random.Random(seed)
    signals = []
    for i in range(count):
        category = rng.choice(CATEGORIES)
        value = round(rng.uniform(25, 96), 1)
        if category == "Risk" and value >= 75:
            severity = "HIGH"
        elif value >= 80:
            severity = "HIGH"
        elif value >= 60:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        titles = {
            "Market": "Market demand movement detected",
            "Competitor": "Competitor activity movement detected",
            "Customer": "Customer behaviour signal detected",
            "Revenue": "Revenue opportunity signal detected",
            "Risk": "Risk indicator movement detected",
        }
        signals.append(LiveSignal(
            timestamp=now(),
            region=rng.choice(REGIONS),
            category=category,
            title=titles[category],
            value=value,
            severity=severity,
            status="NEW"
        ))
    return signals

def kpis(signals):
    high = sum(1 for s in signals if s.severity == "HIGH")
    medium = sum(1 for s in signals if s.severity == "MEDIUM")
    avg = round(sum(s.value for s in signals) / len(signals), 1) if signals else 0
    opportunities = sum(1 for s in signals if s.category == "Revenue" and s.value >= 65)
    return {
        "live_signals": len(signals),
        "high_priority": high,
        "medium_priority": medium,
        "avg_signal_score": avg,
        "opportunities": opportunities,
    }

def action_queue(signals):
    actions = []
    for s in signals:
        if s.severity == "HIGH":
            action = {
                "priority": "URGENT",
                "region": s.region,
                "owner": "Intelligence Team",
                "action": f"Investigate: {s.title}",
                "status": "OPEN"
            }
            actions.append(action)
    return actions
