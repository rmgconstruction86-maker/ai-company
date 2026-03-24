from __future__ import annotations

from src.agents.base import AgentResult, BaseAgent
from src.core.models import Opportunity


class SalesAgent(BaseAgent):
    name = "sales-agent"

    def run(self, opportunity: Opportunity, context: dict) -> AgentResult:
        offer = context.get("offer", {})
        draft = (
            f"Subject: Reducing admin drag for {opportunity.niche} businesses\n\n"
            f"I put together a simple offer for a {offer.get('offer_name', 'productized service')} that can reduce missed follow-up and shorten time-to-cash. "
            f"Core scope: {', '.join(offer.get('deliverables', []))}. "
            f"Estimated implementation window: {offer.get('timeline_days', '?')} days."
        )
        return AgentResult({
            "draft_outreach": draft,
            "channel": "manual-review-email",
            "compliance_note": "Draft only. Human must approve before any outbound contact.",
        })
