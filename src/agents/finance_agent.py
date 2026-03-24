from __future__ import annotations

from src.agents.base import AgentResult, BaseAgent
from src.core.models import Opportunity


class FinanceAgent(BaseAgent):
    name = "finance-agent"

    def run(self, opportunity: Opportunity, context: dict) -> AgentResult:
        score = opportunity.score
        reinvestment_ratio = 0.3 if score < 50 else 0.5 if score < 75 else 0.65
        reserve_ratio = round(1 - reinvestment_ratio, 2)
        return AgentResult({
            "recommended_reinvestment_ratio": reinvestment_ratio,
            "recommended_reserve_ratio": reserve_ratio,
            "max_test_budget": round(min(opportunity.estimated_revenue * 0.1, 250.0), 2),
        })
