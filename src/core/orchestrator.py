from __future__ import annotations

from src.agents.execution_agent import ExecutionAgent
from src.agents.finance_agent import FinanceAgent
from src.agents.market_research import MarketResearchAgent
from src.agents.product_builder import ProductBuilderAgent
from src.agents.sales_agent import SalesAgent
from src.core.models import OpportunityStatus, Task, TaskStatus
from src.core.policy import PolicyEngine
from src.core.scoring import score_opportunity
from src.storage.repo import Repository


class Orchestrator:
    def __init__(self) -> None:
        self.repo = Repository()
        self.policy = PolicyEngine()
        self.research_agent = MarketResearchAgent()
        self.product_agent = ProductBuilderAgent()
        self.sales_agent = SalesAgent()
        self.execution_agent = ExecutionAgent()
        self.finance_agent = FinanceAgent()

    def run_cycle(self) -> dict:
        opportunities = self.repo.list_opportunities()
        processed: list[dict] = []

        for opp in opportunities:
            score = score_opportunity(opp)
            self.repo.update_opportunity(opp.id, score=score, status=OpportunityStatus.scored.value)
            opp.score = score
            opp.status = OpportunityStatus.scored

            decision = self.policy.evaluate_opportunity(opp)
            if not decision.allowed:
                self.repo.update_opportunity(opp.id, status=OpportunityStatus.blocked.value)
                self.repo.add_task(Task(
                    opportunity_id=opp.id,
                    agent_name="policy-engine",
                    title=f"Blocked: {opp.name}",
                    details=decision.reason,
                    status=TaskStatus.blocked,
                    requires_human_approval=True,
                ))
                processed.append({"opportunity": opp.name, "status": "blocked", "reason": decision.reason})
                continue

            research = self.research_agent.run(opp, {})
            offer = self.product_agent.run(opp, {"research": research})
            sales = self.sales_agent.run(opp, {"offer": offer})
            delivery = self.execution_agent.run(opp, {})
            finance = self.finance_agent.run(opp, {})

            task_status = TaskStatus.awaiting_approval if decision.requires_human_approval else TaskStatus.queued

            self.repo.add_task(Task(
                opportunity_id=opp.id,
                agent_name=self.research_agent.name,
                title=f"Research brief for {opp.name}",
                details=str(dict(research)),
                status=task_status,
                requires_human_approval=decision.requires_human_approval,
            ))
            self.repo.add_task(Task(
                opportunity_id=opp.id,
                agent_name=self.product_agent.name,
                title=f"Offer package for {opp.name}",
                details=str(dict(offer)),
                status=task_status,
                requires_human_approval=decision.requires_human_approval,
            ))
            self.repo.add_task(Task(
                opportunity_id=opp.id,
                agent_name=self.sales_agent.name,
                title=f"Outreach draft for {opp.name}",
                details=str(dict(sales)),
                status=TaskStatus.awaiting_approval,
                requires_human_approval=True,
            ))
            self.repo.add_task(Task(
                opportunity_id=opp.id,
                agent_name=self.execution_agent.name,
                title=f"Execution checklist for {opp.name}",
                details=str(dict(delivery)),
                status=TaskStatus.queued,
                requires_human_approval=False,
            ))
            self.repo.add_task(Task(
                opportunity_id=opp.id,
                agent_name=self.finance_agent.name,
                title=f"Budget recommendation for {opp.name}",
                details=str(dict(finance)),
                status=TaskStatus.queued,
                requires_human_approval=False,
            ))

            self.repo.update_opportunity(opp.id, status=OpportunityStatus.planned.value)
            processed.append({
                "opportunity": opp.name,
                "status": "planned",
                "score": score,
                "requires_human_approval": decision.requires_human_approval,
            })

        return {"processed": processed, "metrics": self.repo.metrics().model_dump()}
