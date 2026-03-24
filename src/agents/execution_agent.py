from __future__ import annotations

from src.agents.base import AgentResult, BaseAgent
from src.core.models import Opportunity


class ExecutionAgent(BaseAgent):
    name = "execution-agent"

    def run(self, opportunity: Opportunity, context: dict) -> AgentResult:
        checklist = [
            "create client intake form",
            "define CRM fields",
            "configure follow-up automations",
            "prepare reporting dashboard",
        ]
        return AgentResult({"delivery_plan": checklist})
