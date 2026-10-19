
"""iConnect SA Enterprise AI + Automation Layer.
V4: predictive signals, recommendations, workflows, action tracking and scheduled-report definitions.
Designed to work with demo data now and real data adapters later.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Any
import statistics

@dataclass
class IntelligenceSignal:
    title: str
    category: str
    severity: str
    score: float
    evidence: str
    recommendation: str
    owner: str = "Executive"

@dataclass
class Workflow:
    name: str
    trigger: str
    condition: str
    action: str
    enabled: bool = True

@dataclass
class ActionItem:
    title: str
    priority: str
    owner: str
    due_date: str
    status: str = "Open"

def forecast(values: List[float], periods: int = 3) -> List[float]:
    """Simple transparent trend forecast; replace with ML model when historical data is connected."""
    if not values:
        return [0.0] * periods
    if len(values) == 1:
        return [round(values[0], 2)] * periods
    x = list(range(len(values)))
    xbar, ybar = statistics.mean(x), statistics.mean(values)
    denom = sum((i-xbar)**2 for i in x) or 1
    slope = sum((i-xbar)*(y-ybar) for i, y in zip(x, values)) / denom
    intercept = ybar - slope*xbar
    return [round(intercept + slope*i, 2) for i in range(len(values), len(values)+periods)]

def generate_signals(metrics: Dict[str, float]) -> List[Dict[str, Any]]:
    signals = []
    conversion = metrics.get("conversion_rate", 0)
    growth = metrics.get("market_growth", 0)
    competitor = metrics.get("competitor_activity", 0)
    churn = metrics.get("churn_risk", 0)

    if conversion < 3:
        signals.append(IntelligenceSignal(
            "Conversion performance requires attention", "Performance", "High", 88,
            f"Conversion rate is {conversion:.1f}%.",
            "Review funnel leakage, landing pages and campaign targeting."
        ))
    if growth >= 10:
        signals.append(IntelligenceSignal(
            "High-growth market opportunity detected", "Market", "High", 92,
            f"Market growth is {growth:.1f}%.",
            "Increase acquisition testing and prioritize this market in the next plan."
        ))
    if competitor >= 70:
        signals.append(IntelligenceSignal(
            "Competitor activity elevated", "Competition", "Medium", 76,
            f"Competitive activity index is {competitor:.0f}/100.",
            "Run a competitor positioning review and monitor pricing/content changes."
        ))
    if churn >= 12:
        signals.append(IntelligenceSignal(
            "Customer churn risk elevated", "Customer", "High", 84,
            f"Estimated churn risk is {churn:.1f}%.",
            "Launch retention actions for at-risk customer segments."
        ))
    if not signals:
        signals.append(IntelligenceSignal(
            "No critical intelligence signals detected", "System", "Low", 20,
            "Current monitored metrics are within configured thresholds.",
            "Continue monitoring and refresh connected data sources."
        ))
    return [asdict(s) for s in signals]

def default_workflows() -> List[Dict[str, Any]]:
    return [asdict(x) for x in [
        Workflow("Competitor Threat Alert", "Competitor activity", "> 70", "Create High priority action and notify Executive"),
        Workflow("Growth Opportunity", "Market growth", ">= 10%", "Create opportunity review task"),
        Workflow("Conversion Anomaly", "Conversion rate", "< 3%", "Create funnel investigation task"),
        Workflow("Churn Intervention", "Churn risk", ">= 12%", "Create retention action for Customer team"),
        Workflow("Weekly Executive Brief", "Schedule", "Every Monday", "Generate executive intelligence report"),
    ]]

def create_action(title: str, priority: str, owner: str, days: int = 7) -> Dict[str, Any]:
    return asdict(ActionItem(title, priority, owner, (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")))

def executive_brief(metrics: Dict[str, float]) -> Dict[str, Any]:
    signals = generate_signals(metrics)
    high = [s for s in signals if s["severity"] == "High"]
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "headline": "Enterprise Intelligence Brief",
        "signal_count": len(signals),
        "high_priority_count": len(high),
        "signals": signals,
        "recommended_next_step": high[0]["recommendation"] if high else signals[0]["recommendation"],
    }
