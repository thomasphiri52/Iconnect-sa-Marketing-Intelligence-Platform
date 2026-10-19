from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).isoformat()

@dataclass
class Scenario:
    name: str
    market_growth: float
    revenue_growth: float
    customer_growth: float
    competitor_pressure: float
    investment: float
    projected_revenue: float
    projected_profit: float
    roi: float
    recommendation: str

def simulate(name, base_revenue, margin, market_growth, revenue_growth,
             customer_growth, competitor_pressure, investment):
    # Transparent scenario model for executive planning.
    demand_factor = 1 + (market_growth / 100) * 0.35
    competition_factor = 1 - (competitor_pressure / 100) * 0.18
    revenue = base_revenue * (1 + revenue_growth / 100) * demand_factor * competition_factor
    profit = revenue * (margin / 100) - investment
    roi = ((profit - (base_revenue * margin / 100)) / investment * 100) if investment else 0
    if roi >= 40:
        rec = "Prioritise — strong projected return and manageable competitive pressure."
    elif roi >= 15:
        rec = "Proceed selectively — validate assumptions before scaling investment."
    else:
        rec = "Hold / redesign — projected return does not justify current investment."
    return Scenario(name, market_growth, revenue_growth, customer_growth,
                     competitor_pressure, investment, round(revenue, 2),
                     round(profit, 2), round(roi, 1), rec)

def scenario_pack(base_revenue, margin, investment):
    return [
        simulate("Best Case", base_revenue, margin, 14, 22, 18, 25, investment),
        simulate("Base Case", base_revenue, margin, 8, 12, 10, 45, investment),
        simulate("Downside", base_revenue, margin, 2, 3, 2, 75, investment),
    ]

def expansion_model(province, base_revenue, investment, market_potential, execution_risk):
    uplift = market_potential * (1 - execution_risk / 120)
    projected = base_revenue * (1 + uplift / 100)
    profit = projected * 0.22 - investment
    roi = ((profit - base_revenue * 0.22) / investment * 100) if investment else 0
    return {
        "province": province,
        "market_potential": market_potential,
        "execution_risk": execution_risk,
        "investment": investment,
        "projected_revenue": round(projected, 2),
        "projected_profit": round(profit, 2),
        "roi": round(roi, 1),
        "generated_at": now(),
    }
