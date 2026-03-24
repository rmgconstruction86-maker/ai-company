from __future__ import annotations

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from src.core.config import settings


def get_engine() -> Engine:
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, future=True, connect_args=connect_args)


engine = get_engine()


def init_db() -> None:
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS opportunities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            niche TEXT NOT NULL,
            description TEXT NOT NULL,
            estimated_revenue REAL NOT NULL,
            estimated_effort_hours REAL NOT NULL,
            time_to_cash_days REAL NOT NULL,
            compliance_risk TEXT NOT NULL,
            score REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opportunity_id INTEGER NOT NULL,
            agent_name TEXT NOT NULL,
            title TEXT NOT NULL,
            details TEXT NOT NULL,
            status TEXT NOT NULL,
            requires_human_approval INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(opportunity_id) REFERENCES opportunities(id)
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS agent_variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            variant_name TEXT NOT NULL,
            base_agent TEXT NOT NULL,
            strategy_notes TEXT NOT NULL,
            expected_revenue_lift REAL NOT NULL DEFAULT 0,
            measured_revenue_lift REAL NOT NULL DEFAULT 0,
            evaluation_score REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL,
            created_by TEXT NOT NULL,
            promoted_from_variant_id INTEGER
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS improvement_proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            variant_name TEXT NOT NULL,
            proposal_summary TEXT NOT NULL,
            proposed_patch TEXT NOT NULL,
            safety_notes TEXT NOT NULL,
            projected_gain REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL,
            requires_human_approval INTEGER NOT NULL DEFAULT 1
        )
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            name TEXT DEFAULT '',
            company TEXT DEFAULT '',
            eligible INTEGER NOT NULL DEFAULT 0,
            contacted INTEGER NOT NULL DEFAULT 0
        )
        """))