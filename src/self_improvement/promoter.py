from __future__ import annotations

from src.core.models import ImprovementStatus
from src.storage.repo import Repository


class VariantPromoter:
    def __init__(self) -> None:
        self.repo = Repository()

    def promote_best_eligible_variant(self) -> dict:
        variants = [v for v in self.repo.list_variants() if v.status == ImprovementStatus.approved]
        if not variants:
            return {"status": "no-op", "reason": "No approved variants available."}

        best = max(variants, key=lambda v: (v.evaluation_score, v.measured_revenue_lift))
        self.repo.update_variant(best.id, status=ImprovementStatus.promoted.value)
        return {
            "status": "promoted",
            "variant_name": best.variant_name,
            "evaluation_score": best.evaluation_score,
            "measured_revenue_lift": best.measured_revenue_lift,
        }
