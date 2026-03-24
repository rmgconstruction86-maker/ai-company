from __future__ import annotations

from src.core.models import ImprovementStatus
from src.core.policy import PolicyEngine
from src.self_improvement.evaluator import VariantEvaluator
from src.self_improvement.factory import AgentFactory
from src.self_improvement.promoter import VariantPromoter
from src.storage.repo import Repository


class SelfImprovementController:
    """Bounded improvement loop with explicit approval gates.

    This is not unrestricted recursive self-modification. It only proposes,
    benchmarks, and promotes pre-scoped strategy variants.
    """

    def __init__(self) -> None:
        self.repo = Repository()
        self.policy = PolicyEngine()
        self.factory = AgentFactory()
        self.evaluator = VariantEvaluator()
        self.promoter = VariantPromoter()

    def run_cycle(self, base_agent: str = "orchestrator") -> dict:
        current_variants = self.repo.list_variants()
        parent_id = current_variants[0].id if current_variants else None
        variant, proposal = self.factory.propose_variant(base_agent=base_agent, parent_variant_id=parent_id)

        decision = self.policy.evaluate_improvement(proposal)
        if not decision.allowed:
            proposal.status = ImprovementStatus.rejected
            proposal_id = self.repo.add_improvement_proposal(proposal)
            return {
                "status": "blocked",
                "proposal_id": proposal_id,
                "reason": decision.reason,
            }

        variant_id = self.repo.add_variant(variant)
        proposal_id = self.repo.add_improvement_proposal(proposal)
        benchmark = self.evaluator.evaluate(variant)

        new_status = ImprovementStatus.approved if benchmark["evaluation_score"] >= 0.75 else ImprovementStatus.proposed
        self.repo.update_variant(
            variant_id,
            evaluation_score=benchmark["evaluation_score"],
            measured_revenue_lift=benchmark["measured_revenue_lift"],
            status=new_status.value,
        )
        self.repo.update_improvement_proposal(proposal_id, status=new_status.value)

        promoted = self.promoter.promote_best_eligible_variant()
        return {
            "status": "completed",
            "variant_id": variant_id,
            "proposal_id": proposal_id,
            "benchmark": benchmark,
            "promotion": promoted,
            "note": "All improvements remain bounded by policy and approval rules.",
        }
