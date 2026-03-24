from __future__ import annotations

from dataclasses import dataclass
from src.core.config import settings
from src.core.models import ImprovementProposal, Opportunity, RiskLevel


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str
    requires_human_approval: bool


class PolicyEngine:
    def evaluate_opportunity(self, opportunity: Opportunity) -> PolicyDecision:
        if opportunity.compliance_risk == RiskLevel.high:
            return PolicyDecision(False, "Blocked: high compliance risk opportunity.", True)

        requires_approval = settings.require_human_approval or opportunity.compliance_risk == RiskLevel.medium
        return PolicyDecision(True, "Allowed within current policy rules.", requires_approval)

    def evaluate_improvement(self, proposal: ImprovementProposal) -> PolicyDecision:
        forbidden_terms = [
            "self-replicat",
            "bypass approval",
            "fund transfer",
            "credential harvesting",
            "mass spam",
            "make anything possible",
            "remove policy",
        ]
        combined = f"{proposal.proposal_summary} {proposal.proposed_patch} {proposal.safety_notes}".lower()
        if any(term in combined for term in forbidden_terms):
            return PolicyDecision(False, "Blocked: unsafe self-modification proposal.", True)
        return PolicyDecision(True, "Improvement proposal is eligible for offline evaluation only.", True)
