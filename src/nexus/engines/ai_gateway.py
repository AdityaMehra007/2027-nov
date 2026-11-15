"""
ATLAS NEXUS: Mission 03 - AI Model Gateway, Swarm Runtime & Episodic Memory
Dynamic multi-model routing, fallback resilience, consensus voting, and memory stores.
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ModelTier(str, Enum):
    FAST = "FAST"
    REASONING = "REASONING"
    EMBEDDING = "EMBEDDING"
    LOCAL = "LOCAL"


@dataclass
class RouteDecision:
    model_id: str
    tier: ModelTier
    max_tokens: int


class ModelGateway:
    def __init__(self) -> None:
        self.primary_models = {
            ModelTier.FAST: "gemini-3.8-flash",
            ModelTier.REASONING: "gemini-3.1-pro-thinking",
            ModelTier.EMBEDDING: "text-embedding-004",
            ModelTier.LOCAL: "llama-3.3-70b-instruct",
        }
        self.fallback_models = {
            ModelTier.FAST: "gpt-4o-mini",
            ModelTier.REASONING: "claude-3-7-sonnet",
        }

    def route_task(self, task_type: str, prompt: str) -> RouteDecision:
        tier = ModelTier.FAST
        max_tokens = 4096

        normalized = task_type.upper()
        if "REASON" in normalized or len(prompt) > 2000 or "proof" in prompt.lower():
            tier = ModelTier.REASONING
            max_tokens = 16384
        elif "EMBED" in normalized:
            tier = ModelTier.EMBEDDING
            max_tokens = 1024
        elif "LOCAL" in normalized:
            tier = ModelTier.LOCAL
            max_tokens = 8192

        model_id = self.primary_models.get(tier, "gemini-3.8-flash")
        return RouteDecision(model_id=model_id, tier=tier, max_tokens=max_tokens)

    def execute_with_fallback(
        self,
        failing_primary: bool = False,
        prompt: str = "",
        tier: ModelTier = ModelTier.FAST,
    ) -> Dict[str, Any]:
        if failing_primary:
            fallback_model = self.fallback_models.get(tier, "claude-3-7-sonnet")
            return {
                "status": "SUCCESS_VIA_FALLBACK",
                "model_used": fallback_model,
                "output": f"Processed via resilient fallback model: {fallback_model}",
            }
        primary_model = self.primary_models.get(tier, "gemini-3.8-flash")
        return {
            "status": "SUCCESS",
            "model_used": primary_model,
            "output": f"Processed via primary model: {primary_model}",
        }


@dataclass
class AgentVote:
    agent_id: str
    vote: str
    confidence: float


@dataclass
class ConsensusResult:
    decision: str
    approval_ratio: float
    quorum_achieved: bool


class SwarmRuntime:
    def evaluate_consensus(self, votes: List[AgentVote]) -> ConsensusResult:
        if not votes:
            return ConsensusResult(decision="REJECT", approval_ratio=0.0, quorum_achieved=False)

        total_weight = sum(v.confidence for v in votes)
        approvals = sum(v.confidence for v in votes if v.vote.upper() == "APPROVE")

        ratio = approvals / total_weight if total_weight > 0 else 0.0
        quorum = len(votes) >= 3 and ratio >= 0.50
        decision = "APPROVE" if ratio >= 0.50 else "REJECT"

        return ConsensusResult(
            decision=decision,
            approval_ratio=ratio,
            quorum_achieved=quorum,
        )


class EpisodicMemoryStore:
    def __init__(self) -> None:
        self._store: Dict[str, Dict[str, Any]] = {}

    def store(self, key: str, content: str, tags: Optional[List[str]] = None) -> None:
        self._store[key] = {
            "key": key,
            "content": content,
            "tags": [t.lower() for t in (tags or [])],
            "timestamp": time.time(),
        }

    def query(
        self,
        tag: Optional[str] = None,
        keyword: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = []
        for item in self._store.values():
            match = True
            if tag and tag.lower() not in item["tags"]:
                match = False
            if keyword and keyword.lower() not in item["content"].lower():
                match = False
            if match:
                results.append(item)
        return results
