from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Autonomous AI Company")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./autonomous_ai_company.db")
    default_daily_budget: float = float(os.getenv("DEFAULT_DAILY_BUDGET", "250.0"))
    require_human_approval: bool = os.getenv("REQUIRE_HUMAN_APPROVAL", "true").lower() == "true"


settings = Settings()
