from __future__ import annotations

from typing import Any
from sqlalchemy import text
from src.storage.db import engine
from src.core.models import (
    AgentVariant,
    ImprovementProposal,
    ImprovementStatus,
    MetricSnapshot,
    Opportunity,
    OpportunityStatus,
    Task,
    TaskStatus,
)


class Repository:
    def add_opportunity(self, opportunity: Opportunity) -> int:
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                INSERT INTO opportunities
                (name, niche, description, estimated_revenue, estimated_effort_hours, time_to_cash_days, compliance_risk, score, status)
                VALUES (:name, :niche, :description, :estimated_revenue, :estimated_effort_hours, :time_to_cash_days, :compliance_risk, :score, :status)
                """),
                opportunity.model_dump(exclude={"id"}),
            )
            return int(result.lastrowid)

    def list_opportunities(self) -> list[Opportunity]:
        with engine.begin() as conn:
            rows = conn.execute(text("SELECT * FROM opportunities ORDER BY score DESC, id ASC")).mappings().all()
        return [Opportunity(**dict(r)) for r in rows]

    def update_opportunity(self, opportunity_id: int, **fields: Any) -> None:
        if not fields:
            return
        assignments = ", ".join(f"{k} = :{k}" for k in fields)
        params = {**fields, "id": opportunity_id}
        with engine.begin() as conn:
            conn.execute(text(f"UPDATE opportunities SET {assignments} WHERE id = :id"), params)

    def add_task(self, task: Task) -> int:
        payload = task.model_dump(exclude={"id"})
        payload["requires_human_approval"] = 1 if payload["requires_human_approval"] else 0
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                INSERT INTO tasks
                (opportunity_id, agent_name, title, details, status, requires_human_approval)
                VALUES (:opportunity_id, :agent_name, :title, :details, :status, :requires_human_approval)
                """),
                payload,
            )
            return int(result.lastrowid)

    def list_tasks(self) -> list[Task]:
        with engine.begin() as conn:
            rows = conn.execute(text("SELECT * FROM tasks ORDER BY id ASC")).mappings().all()
        tasks: list[Task] = []
        for row in rows:
            data = dict(row)
            data["requires_human_approval"] = bool(data["requires_human_approval"])
            tasks.append(Task(**data))
        return tasks

    def add_variant(self, variant: AgentVariant) -> int:
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                INSERT INTO agent_variants
                (variant_name, base_agent, strategy_notes, expected_revenue_lift, measured_revenue_lift, evaluation_score, status, created_by, promoted_from_variant_id)
                VALUES (:variant_name, :base_agent, :strategy_notes, :expected_revenue_lift, :measured_revenue_lift, :evaluation_score, :status, :created_by, :promoted_from_variant_id)
                """),
                variant.model_dump(exclude={"id"}),
            )
            return int(result.lastrowid)

    def list_variants(self) -> list[AgentVariant]:
        with engine.begin() as conn:
            rows = conn.execute(text("SELECT * FROM agent_variants ORDER BY evaluation_score DESC, id ASC")).mappings().all()
        return [AgentVariant(**dict(r)) for r in rows]

    def update_variant(self, variant_id: int, **fields: Any) -> None:
        if not fields:
            return
        assignments = ", ".join(f"{k} = :{k}" for k in fields)
        params = {**fields, "id": variant_id}
        with engine.begin() as conn:
            conn.execute(text(f"UPDATE agent_variants SET {assignments} WHERE id = :id"), params)

    def add_improvement_proposal(self, proposal: ImprovementProposal) -> int:
        payload = proposal.model_dump(exclude={"id"})
        payload["requires_human_approval"] = 1 if payload["requires_human_approval"] else 0
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                INSERT INTO improvement_proposals
                (variant_name, proposal_summary, proposed_patch, safety_notes, projected_gain, status, requires_human_approval)
                VALUES (:variant_name, :proposal_summary, :proposed_patch, :safety_notes, :projected_gain, :status, :requires_human_approval)
                """),
                payload,
            )
            return int(result.lastrowid)

    def list_improvement_proposals(self) -> list[ImprovementProposal]:
        with engine.begin() as conn:
            rows = conn.execute(text("SELECT * FROM improvement_proposals ORDER BY id ASC")).mappings().all()
        proposals: list[ImprovementProposal] = []
        for row in rows:
            data = dict(row)
            data["requires_human_approval"] = bool(data["requires_human_approval"])
            proposals.append(ImprovementProposal(**data))
        return proposals

    def update_improvement_proposal(self, proposal_id: int, **fields: Any) -> None:
        if not fields:
            return
        assignments = ", ".join(f"{k} = :{k}" for k in fields)
        params = {**fields, "id": proposal_id}
        with engine.begin() as conn:
            conn.execute(text(f"UPDATE improvement_proposals SET {assignments} WHERE id = :id"), params)

    def metrics(self) -> MetricSnapshot:
        opportunities = self.list_opportunities()
        tasks = self.list_tasks()
        total_tasks = len(tasks)
        blocked_tasks = sum(1 for t in tasks if t.status == TaskStatus.blocked)
        pending_approvals = sum(1 for t in tasks if t.status == TaskStatus.awaiting_approval)
        projected_revenue = sum(o.estimated_revenue for o in opportunities if o.status != OpportunityStatus.blocked)
        average_score = (sum(o.score for o in opportunities) / len(opportunities)) if opportunities else 0.0
        return MetricSnapshot(
            total_opportunities=len(opportunities),
            total_tasks=total_tasks,
            blocked_tasks=blocked_tasks,
            pending_approvals=pending_approvals,
            projected_revenue=projected_revenue,
            average_score=average_score,
        )
