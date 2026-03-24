from __future__ import annotations

from src.core.models import AgentVariant, ImprovementProposal, ImprovementStatus


class AgentFactory:
    """Creates bounded strategy variants. It does not create unrestricted new AIs."""

    def propose_variant(self, base_agent: str, parent_variant_id: int | None = None) -> tuple[AgentVariant, ImprovementProposal]:
        variant_name = f"{base_agent}-variant-{parent_variant_id or 'seed'}"
        strategy_notes = (
            "Tighten qualification criteria, shorten proposal cycle, and prioritize niches "
            "with faster time-to-cash and lower delivery complexity."
        )
        projected_gain = 0.08
        variant = AgentVariant(
            variant_name=variant_name,
            base_agent=base_agent,
            strategy_notes=strategy_notes,
            expected_revenue_lift=projected_gain,
            evaluation_score=0.0,
            status=ImprovementStatus.proposed,
            created_by="agent-factory",
            promoted_from_variant_id=parent_variant_id,
        )
        proposal = ImprovementProposal(
            variant_name=variant_name,
            proposal_summary="Propose a tighter revenue-optimization strategy variant for offline testing.",
            proposed_patch=(
                "Modify ranking weights toward short sales cycles, high close probability, "
                "and repeatable productized delivery. Keep policy gates intact."
            ),
            safety_notes="Offline evaluation only. No autonomous deployment without approval.",
            projected_gain=projected_gain,
            status=ImprovementStatus.proposed,
            requires_human_approval=True,
        )
        return variant, proposal
