from __future__ import annotations

from src.core.models import Opportunity, RiskLevel


RISK_PENALTY = {
    RiskLevel.low: 5,
    RiskLevel.medium: 20,
    RiskLevel.high: 45,
}


def score_opportunity(opportunity: Opportunity) -> float:
    revenue_component = min(opportunity.estimated_revenue / 100.0, 60)
    effort_penalty = min(opportunity.estimated_effort_hours * 1.8, 25)
    speed_bonus = max(0, 25 - opportunity.time_to_cash_days * 3)
    risk_penalty = RISK_PENALTY[opportunity.compliance_risk]
    raw = revenue_component + speed_bonus - effort_penalty - risk_penalty + 40
    return round(max(raw, 0), 2)
