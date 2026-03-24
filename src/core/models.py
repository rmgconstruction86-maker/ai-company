from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class OpportunityStatus(str, Enum):
    new = "new"
    scored = "scored"
    blocked = "blocked"
    planned = "planned"
    executed = "executed"


class TaskStatus(str, Enum):
    queued = "queued"
    awaiting_approval = "awaiting_approval"
    completed = "completed"
    blocked = "blocked"


class ImprovementStatus(str, Enum):
    proposed = "proposed"
    approved = "approved"
    rejected = "rejected"
    promoted = "promoted"


class Opportunity(BaseModel):
    id: int | None = None
    name: str
    niche: str
    description: str
    estimated_revenue: float = Field(ge=0)
    estimated_effort_hours: float = Field(ge=0)
    time_to_cash_days: float = Field(ge=0)
    compliance_risk: RiskLevel = RiskLevel.low
    score: float = 0.0
    status: OpportunityStatus = OpportunityStatus.new


class Task(BaseModel):
    id: int | None = None
    opportunity_id: int
    agent_name: str
    title: str
    details: str
    status: TaskStatus = TaskStatus.queued
    requires_human_approval: bool = False


class MetricSnapshot(BaseModel):
    total_opportunities: int
    total_tasks: int
    blocked_tasks: int
    pending_approvals: int
    projected_revenue: float
    average_score: float


class AgentVariant(BaseModel):
    id: int | None = None
    variant_name: str
    base_agent: str
    strategy_notes: str
    expected_revenue_lift: float = 0.0
    measured_revenue_lift: float = 0.0
    evaluation_score: float = 0.0
    status: ImprovementStatus = ImprovementStatus.proposed
    created_by: str = "agent-factory"
    promoted_from_variant_id: int | None = None


class ImprovementProposal(BaseModel):
    id: int | None = None
    variant_name: str
    proposal_summary: str
    proposed_patch: str
    safety_notes: str
    projected_gain: float = 0.0
    status: ImprovementStatus = ImprovementStatus.proposed
    requires_human_approval: bool = True
