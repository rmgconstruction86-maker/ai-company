from __future__ import annotations

from fastapi import FastAPI, HTTPException
from src.core.config import settings
from src.core.models import Opportunity, RiskLevel
from src.core.orchestrator import Orchestrator
from src.core.self_improvement import SelfImprovementController
from src.storage.db import init_db
from src.storage.repo import Repository

app = FastAPI(title=settings.app_name)
repo = Repository()
orchestrator = Orchestrator()
self_improver = SelfImprovementController()


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name}


@app.post("/seed-demo")
def seed_demo() -> dict:
    demo = [
        Opportunity(
            name="Contractor lead follow-up automation",
            niche="home services",
            description="Automate estimate requests, follow-up, and missed-call recovery.",
            estimated_revenue=4000,
            estimated_effort_hours=8,
            time_to_cash_days=5,
            compliance_risk=RiskLevel.low,
        ),
        Opportunity(
            name="Local clinic FAQ assistant",
            niche="healthcare admin",
            description="Patient intake FAQ assistant with scheduling handoff. Requires careful compliance review.",
            estimated_revenue=6500,
            estimated_effort_hours=14,
            time_to_cash_days=10,
            compliance_risk=RiskLevel.medium,
        ),
        Opportunity(
            name="Aggressive bulk cold outreach dataset",
            niche="unknown scraped leads",
            description="High-risk mass outreach concept intentionally included to demonstrate blocking.",
            estimated_revenue=12000,
            estimated_effort_hours=4,
            time_to_cash_days=2,
            compliance_risk=RiskLevel.high,
        ),
    ]
    ids = [repo.add_opportunity(item) for item in demo]
    return {"seeded_ids": ids}


@app.post("/opportunities")
def create_opportunity(opportunity: Opportunity) -> dict:
    new_id = repo.add_opportunity(opportunity)
    return {"id": new_id}


@app.get("/opportunities")
def list_opportunities() -> list[dict]:
    return [o.model_dump() for o in repo.list_opportunities()]


@app.get("/tasks")
def list_tasks() -> list[dict]:
    return [t.model_dump() for t in repo.list_tasks()]


@app.get("/metrics")
def metrics() -> dict:
    return repo.metrics().model_dump()


@app.get("/variants")
def variants() -> list[dict]:
    return [v.model_dump() for v in repo.list_variants()]


@app.get("/improvement-proposals")
def improvement_proposals() -> list[dict]:
    return [p.model_dump() for p in repo.list_improvement_proposals()]


@app.post("/run-cycle")
def run_cycle() -> dict:
    return orchestrator.run_cycle()


@app.post("/run-self-improvement")
def run_self_improvement(base_agent: str = "orchestrator") -> dict:
    return self_improver.run_cycle(base_agent=base_agent)


@app.post("/leads/{lead_id}/auto-send")
def auto_send(lead_id: int) -> dict:
    lead = repo.get_lead(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if not getattr(lead, "eligible", False):
        raise HTTPException(status_code=400, detail="Lead not eligible")

    if getattr(lead, "contacted", False):
        return {"message": "Already contacted"}

    subject = "Quick question about missed calls"

    body = f"""Hi {lead.name or ''},

Do you have anything automatically following up on missed calls?

We help contractors capture more jobs automatically.

Want a quick demo?

– Tyler
"""

    print(f"Sending email to {lead.email}")
    repo.mark_lead_contacted(lead_id)

    return {
        "message": "Auto-sent",
        "subject": subject,
        "body": body,
    }
from fastapi import HTTPException

@app.post("/leads")
def create_lead(email: str, name: str = "", company: str = ""):
    lead_id = repo.add_lead(email=email, name=name, company=company)
    return {"id": lead_id}


@app.get("/leads")
def list_leads():
    return repo.list_leads()


@app.post("/leads/{lead_id}/eligible")
def set_eligible(lead_id: int, eligible: bool = True):
    repo.set_lead_eligible(lead_id, eligible)
    return {"status": "updated"}


@app.post("/leads/{lead_id}/auto-send")
def auto_send(lead_id: int):
    lead = repo.get_lead(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if not lead["eligible"]:
        raise HTTPException(status_code=400, detail="Lead not eligible")

    if lead["contacted"]:
        return {"message": "Already contacted"}

    subject = "Quick question about missed calls"

    body = f"""Hi {lead.get("name","")},

Do you have anything automatically following up on missed calls?

We help contractors capture more jobs automatically.

Want a quick demo?

– Tyler
"""

    print(f"Sending email to {lead['email']}")

    repo.mark_lead_contacted(lead_id)

    return {
        "message": "Auto-sent",
        "subject": subject,
        "body": body
    }
from fastapi import HTTPException

@app.post("/leads")
def create_lead(email: str, name: str = "", company: str = ""):
    lead_id = repo.add_lead(email=email, name=name, company=company)
    return {"id": lead_id}


@app.get("/leads")
def list_leads():
    return repo.list_leads()


@app.post("/leads/{lead_id}/eligible")
def set_eligible(lead_id: int, eligible: bool = True):
    repo.set_lead_eligible(lead_id, eligible)
    return {"status": "updated"}


@app.post("/leads/{lead_id}/auto-send")
def auto_send(lead_id: int):
    lead = repo.get_lead(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if not lead["eligible"]:
        raise HTTPException(status_code=400, detail="Lead not eligible")

    if lead["contacted"]:
        return {"message": "Already contacted"}

    subject = "Quick question about missed calls"

    body = f"""Hi {lead.get("name","")},

Do you have anything automatically following up on missed calls?

We help contractors capture more jobs automatically.

Want a quick demo?

– Tyler
"""

    print(f"Sending email to {lead['email']}")

    repo.mark_lead_contacted(lead_id)

    return {
        "message": "Auto-sent",
        "subject": subject,
        "body": body
    }
from fastapi import HTTPException

@app.post("/leads")
def create_lead(email: str, name: str = "", company: str = ""):
    lead_id = repo.add_lead(email=email, name=name, company=company)
    return {"id": lead_id}


@app.get("/leads")
def list_leads():
    return repo.list_leads()


@app.post("/leads/{lead_id}/eligible")
def set_eligible(lead_id: int, eligible: bool = True):
    repo.set_lead_eligible(lead_id, eligible)
    return {"status": "updated"}


@app.post("/leads/{lead_id}/auto-send")
def auto_send(lead_id: int):
    lead = repo.get_lead(lead_id)

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if not lead["eligible"]:
        raise HTTPException(status_code=400, detail="Lead not eligible")

    if lead["contacted"]:
        return {"message": "Already contacted"}

    subject = "Quick question about missed calls"

    body = f"""Hi {lead.get("name","")},

Do you have anything automatically following up on missed calls?

We help contractors capture more jobs automatically.

Want a quick demo?

– Tyler
"""

    print(f"Sending email to {lead['email']}")

    repo.mark_lead_contacted(lead_id)

    return {
        "message": "Auto-sent",
        "subject": subject,
        "body": body
    }
