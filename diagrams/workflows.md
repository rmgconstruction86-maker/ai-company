# Workflow Diagrams

## 1) End-to-end orchestration flow

```mermaid
flowchart TD
    A[Scheduler / API Trigger] --> B[Load Opportunities]
    B --> C[Score Opportunities]
    C --> D{Policy Gate}
    D -- rejected --> E[Log rejection]
    D -- approved --> F[Create Tasks]
    F --> G[Route to Agent]
    G --> H[Generate Output / Action Plan]
    H --> I{Needs Human Approval?}
    I -- yes --> J[Queue Approval]
    I -- no --> K[Execute Allowed Action]
    K --> L[Record Result]
    J --> L
    L --> M[Update Metrics]
    M --> N[Budget Reallocation]
```

## 2) Opportunity scoring pipeline

```mermaid
flowchart LR
    A[Opportunity] --> B[Revenue Potential]
    A --> C[Delivery Complexity]
    A --> D[Time to Cash]
    A --> E[Compliance Risk]
    B --> F[Weighted Score]
    C --> F
    D --> F
    E --> F
    F --> G[Priority Queue]
```

## 3) Agent interaction model

```mermaid
sequenceDiagram
    participant API
    participant Orch as Orchestrator
    participant Policy
    participant Score
    participant Research
    participant Product
    participant Sales
    participant Finance
    participant DB

    API->>Orch: run_cycle()
    Orch->>DB: fetch_opportunities()
    DB-->>Orch: opportunities
    Orch->>Score: rank(opportunities)
    Score-->>Orch: ranked list

    loop each opportunity
        Orch->>Policy: evaluate(opportunity)
        Policy-->>Orch: allowed / blocked
        alt allowed
            Orch->>Research: analyze(opportunity)
            Research-->>Orch: research brief
            Orch->>Product: create_offer(research brief)
            Product-->>Orch: offer package
            Orch->>Sales: draft_outreach(offer package)
            Sales-->>Orch: safe draft
            Orch->>Finance: propose_allocation(opportunity)
            Finance-->>Orch: allocation plan
            Orch->>DB: save tasks + metrics
        else blocked
            Orch->>DB: save policy rejection
        end
    end
```

## 4) Revenue loop

```mermaid
flowchart TD
    A[Leads / Demand Signals] --> B[Qualified Opportunities]
    B --> C[Offers]
    C --> D[Proposals / Draft Outreach]
    D --> E[Closed Deals]
    E --> F[Delivery]
    F --> G[Collected Revenue]
    G --> H[Reserve + Reinvestment]
    H --> A
```

## 5) Bounded self-improvement loop

```mermaid
flowchart TD
    A[Run self-improvement cycle] --> B[AgentFactory proposes scoped variant]
    B --> C[PolicyEngine checks proposal]
    C -->|blocked| D[Reject and log proposal]
    C -->|allowed| E[Offline benchmark]
    E --> F{Score threshold met?}
    F -->|no| G[Keep as proposed]
    F -->|yes| H[Mark approved]
    H --> I[Promote best approved variant]
    I --> J[Update active strategy]
```

## 6) Variant lineage

```mermaid
flowchart LR
    A[Base agent strategy] --> B[Variant 1]
    B --> C[Variant 2]
    C --> D[Variant 3]
    D --> E[Promoted active variant]
```
