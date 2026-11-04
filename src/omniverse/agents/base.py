from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import time

class AgentTask(BaseModel):
    task_type: str
    payload: Dict[str, Any]
    created_at: float = Field(default_factory=time.time)

class BaseAgent(ABC):
    """Abstract base class for all Omniverse virtual agents."""

    @property
    @abstractmethod
    def role_name(self) -> str:
        pass

    @property
    @abstractmethod
    def division(self) -> str:
        pass

    @abstractmethod
    def execute_task(self, task: AgentTask) -> Dict[str, Any]:
        pass

class AgentDispatcher:
    """Manages agent registrations and task dispatching."""

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent) -> None:
        self._agents[agent.role_name] = agent

    def dispatch(self, agent_name: str, task: AgentTask) -> Dict[str, Any]:
        agent = self._agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not registered")
        return agent.execute_task(task)

    def list_agents(self) -> Dict[str, str]:
        return {name: agent.division for name, agent in self._agents.items()}
