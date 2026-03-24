# Autonomous AI Company Starter

This is a lawful, guardrailed starter system for a mostly autonomous AI-operated business.

It is **not** configured to pursue impossible targets like doubling revenue every day indefinitely, and it does **not** implement unrestricted recursive self-replication. Instead, it is built to:

- run specialized agents,
- score opportunities,
- generate tasks,
- execute approved workflows,
- measure ROI,
- reallocate budget based on performance,
- propose bounded strategy variants,
- benchmark those variants offline,
- promote only approved improvements.

## What it does

- Maintains an internal opportunity backlog
- Scores opportunities with a configurable strategy
- Routes work to agents:
  - market research
  - product generation
  - sales drafting
  - execution planner
  - finance allocator
- Enforces policy constraints before execution
- Exposes a FastAPI control surface
- Persists state in SQLite
- Adds a **bounded self-improvement loop** that creates strategy variants rather than unrestricted new AIs

## What it does not do

- no bulk spam sending
- no hidden credential scraping
- no autonomous fund transfers
- no autonomous contract signing
- no unrestricted self-rewriting without approval
- no "make anything possible" general autonomy claims

## Self-improvement design

The self-improvement loop works like this:

1. `AgentFactory` proposes a new variant of a scoped agent strategy.
2. `PolicyEngine` checks the proposal for forbidden behaviors.
3. `VariantEvaluator` benchmarks the variant on safe proxy metrics.
4. Only high-scoring variants are marked approved.
5. `VariantPromoter` promotes the best approved variant.

This is closer to **controlled continuous optimization** than open-ended recursive AGI.

## Project layout

```text
src/
  api/
    app.py
  agents/
    base.py
    market_research.py
    product_builder.py
    sales_agent.py
    execution_agent.py
    finance_agent.py
  core/
    config.py
    models.py
    policy.py
    orchestrator.py
    self_improvement.py
    scoring.py
  self_improvement/
    factory.py
    evaluator.py
    promoter.py
  storage/
    db.py
    repo.py
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.api.app:app --reload
```

Then call:

- `GET /health`
- `POST /seed-demo`
- `POST /run-cycle`
- `POST /run-self-improvement`
- `GET /variants`
- `GET /improvement-proposals`
- `GET /tasks`
- `GET /metrics`

## Example usage

```bash
curl -X POST http://127.0.0.1:8000/seed-demo
curl -X POST http://127.0.0.1:8000/run-cycle
curl -X POST 'http://127.0.0.1:8000/run-self-improvement?base_agent=orchestrator'
curl http://127.0.0.1:8000/variants
curl http://127.0.0.1:8000/improvement-proposals
```

## How to make it real

Replace the stubs with actual integrations:

- CRM / database: HubSpot, Supabase, Postgres
- LLM provider: OpenAI Responses API or equivalent
- Email drafts: Gmail or transactional provider with approval gates
- Payments: Stripe for lawful billing
- Analytics: PostHog, Metabase, or custom warehouse
- Ads: Meta / Google APIs only if you have approval and budget controls

Do not remove policy gates unless you understand the legal and operational consequences.
