from __future__ import annotations

from src.agents.base import AgentResult, BaseAgent
from src.core.models import Opportunity


class MarketResearchAgent(BaseAgent):
    name = "market-research"

    def run(self, opportunity: Opportunity, context: dict) -> AgentResult:
        problem = f"Businesses in {opportunity.niche} often lose time or revenue due to inconsistent follow-up, quoting, and admin workflows."
        angle = f"Offer a productized AI automation package for {opportunity.niche} with fast implementation and clear ROI."
        return AgentResult({
            "problem_summary": problem,
            "offer_angle": angle,
            "price_anchor": round(max(opportunity.estimated_revenue * 0.15, 500), 2),
        })
