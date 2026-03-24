from __future__ import annotations

from src.core.models import AgentVariant


class VariantEvaluator:
    """Toy evaluator for offline benchmarking against safe business metrics."""

    def evaluate(self, variant: AgentVariant) -> dict:
        notes = variant.strategy_notes.lower()
        score = 0.5
        if "faster time-to-cash" in notes:
            score += 0.15
        if "lower delivery complexity" in notes:
            score += 0.1
        if "qualification" in notes:
            score += 0.1
        measured_lift = min(max(score - 0.5, 0.0), 0.25)
        return {
            "evaluation_score": round(score, 4),
            "measured_revenue_lift": round(measured_lift, 4),
            "benchmark_notes": "Offline benchmark based on safe proxy metrics only.",
        }
