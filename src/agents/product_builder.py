from __future__ import annotations

from src.agents.base import AgentResult, BaseAgent
from src.core.models import Opportunity


class ProductBuilderAgent(BaseAgent):
    name = "product-builder"

    def run(self, opportunity: Opportunity, context: dict) -> AgentResult:
        research = context.get("research", {})
        offer = {
            "offer_name": f"{opportunity.niche.title()} AI Operations Package",
            "deliverables": [
                "lead intake workflow",
                "quote follow-up automation",
                "customer FAQ assistant",
                "weekly KPI report",
            ],
            "price": research.get("price_anchor", 750.0),
            "timeline_days": max(2, int(opportunity.time_to_cash_days)),
        }
        return AgentResult(offer)
