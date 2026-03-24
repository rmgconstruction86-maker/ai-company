from __future__ import annotations

from abc import ABC, abstractmethod
from src.core.models import Opportunity


class AgentResult(dict):
    pass


class BaseAgent(ABC):
    name: str = "base-agent"

    @abstractmethod
    def run(self, opportunity: Opportunity, context: dict) -> AgentResult:
        raise NotImplementedError
