from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from statistics import mean
from typing import List, Dict

def now():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class IntelligenceSignal:
    title: str
    category: str
    severity: str
    score: float
    recommendation: str
    rationale: str
    created_at: str

def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, float(v)))

def opportunity_score(demand, growth, customer_fit, competition, revenue):
    return round(
        clamp(
            demand * 0.25 +
            growth * 0.20 +
            customer_fit * 0.20 +
            (100 - competition) * 0.15 +
            revenue * 0.20
        ), 1
    )

def competitor_threat(activity, momentum, pricing_pressure):
    return round(clamp(activity * .4 + momentum * .35 + pricing_pressure * .25), 1)

def churn_risk(usage_drop, support_pressure, payment_risk):
    return round(clamp(usage_drop * .45 + support_pressure * .30 + payment_risk * .25), 1)

def forecast(values, periods=4):
    values = [float(v) for v in values if v is not None]
    if len(values) < 2:
        return []
    slope = (values[-1] - values[0]) / (len(values) - 1)
    base = values[-1]
    return [round(base + slope * i, 2) for i in range(1, periods + 1)]

def generate_signals(metrics: Dict[str, float]) -> List[IntelligenceSignal]:
    signals = []
    opp = opportunity_score(
        metrics.get("demand", 0), metrics.get("growth", 0) * 10,
        metrics.get("customer_fit", 0), metrics.get("competition", 0),
        metrics.get("revenue_potential", 0)
    )
    threat = competitor_threat(
        metrics.get("competitor_activity", 0),
        metrics.get("competitor_momentum", 0),
        metrics.get("pricing_pressure", 0)
    )
    churn = churn_risk(
        metrics.get("usage_drop", 0),
        metrics.get("support_pressure", 0),
        metrics.get("payment_risk", 0)
    )

    if opp >= 75:
        signals.append(IntelligenceSignal(
            "High-value growth opportunity", "Opportunity", "HIGH", opp,
            "Prioritise this market segment and launch a targeted growth action.",
            f"Opportunity score is {opp}/100 based on demand, growth, fit, competition and revenue potential.", now()
        ))
    if threat >= 70:
        signals.append(IntelligenceSignal(
            "Competitor movement detected", "Threat", "HIGH", threat,
            "Review competitor positioning, pricing and campaign activity immediately.",
            f"Competitive threat score is {threat}/100.", now()
        ))
    if churn >= 65:
        signals.append(IntelligenceSignal(
            "Customer churn risk", "Customer", "HIGH", churn,
            "Trigger retention outreach and investigate usage/support drivers.",
            f"Churn risk score is {churn}/100.", now()
        ))
    if not signals:
        signals.append(IntelligenceSignal(
            "Stable intelligence environment", "Monitoring", "LOW", 42,
            "Continue monitoring and refresh intelligence data on schedule.",
            "No configured high-priority threshold has been breached.", now()
        ))
    return signals

def executive_brief(signals: List[IntelligenceSignal]):
    high = [s for s in signals if s.severity == "HIGH"]
    lines = [
        "iConnect SA Executive Intelligence Brief",
        f"Generated: {now()}",
        f"Signals detected: {len(signals)}",
        f"High-priority signals: {len(high)}",
        ""
    ]
    for s in signals:
        lines.append(f"- {s.title} | {s.severity} | Score {s.score}/100")
        lines.append(f"  Recommendation: {s.recommendation}")
    return "\n".join(lines)
