import math
import hashlib
from typing import Dict, List, Tuple, Optional


def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculates cosine similarity between two float vectors."""
    if len(v1) != len(v2) or not v1:
        return 0.0

    dot = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    return dot / (norm_a * norm_b)


class SemanticCache:
    """Hybrid O(1) Exact Hash and Cosine-Vector Semantic Cache."""

    def __init__(self, similarity_threshold: float = 0.90, max_entries: int = 1000):
        self.similarity_threshold = similarity_threshold
        self.max_entries = max_entries
        self.exact_cache: Dict[str, str] = {}
        self.vector_entries: List[Tuple[str, str, List[float]]] = []

    def _hash_key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.strip().lower().encode("utf-8")).hexdigest()

    def get(
        self,
        prompt: str,
        embedding: Optional[List[float]] = None,
    ) -> Tuple[bool, Optional[str], bool]:
        """
        Lookup prompt in cache.
        Returns:
            (hit: bool, response: Optional[str], is_semantic: bool)
        """
        # Tier 1: O(1) Exact Match Hit
        key = self._hash_key(prompt)
        if key in self.exact_cache:
            return True, self.exact_cache[key], False

        # Tier 2: Vector Cosine Semantic Hit
        if embedding:
            best_sim = -1.0
            best_response: Optional[str] = None
            for p_cached, r_cached, emb_cached in self.vector_entries:
                sim = cosine_similarity(embedding, emb_cached)
                if sim > best_sim:
                    best_sim = sim
                    best_response = r_cached

            if best_sim >= self.similarity_threshold and best_response is not None:
                return True, best_response, True

        return False, None, False

    def set(
        self,
        prompt: str,
        response: str,
        embedding: Optional[List[float]] = None,
    ) -> None:
        """Stores a prompt-response pair with optional vector embedding."""
        key = self._hash_key(prompt)
        self.exact_cache[key] = response

        if embedding:
            if len(self.vector_entries) >= self.max_entries:
                self.vector_entries.pop(0)
            self.vector_entries.append((prompt, response, embedding))

    def clear(self) -> None:
        self.exact_cache.clear()
        self.vector_entries.clear()
