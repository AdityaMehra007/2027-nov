import math
from dataclasses import dataclass
from typing import List, Dict, Any
from .index import InvertedIndex
from .tokenizer import tokenize

@dataclass
class SearchResult:
    doc_id: int
    score: float
    metadata: Dict[str, Any]

class BM25Ranker:
    def __init__(self, index: InvertedIndex, k1: float = 1.5, b: float = 0.75):
        self.index = index
        self.k1 = k1
        self.b = b

    def _idf(self, term: str) -> float:
        """Computes inverse document frequency for a term with smoothing."""
        n = len(self.index.get_postings(term))
        N = self.index.total_documents
        if N == 0:
            return 0.0
        return math.log(1.0 + (N - n + 0.5) / (n + 0.5))

    def search(self, query: str, top_k: int = 10) -> List[SearchResult]:
        """Calculates BM25 scores for matching documents and returns ranked results."""
        query_terms = tokenize(query)
        if not query_terms or self.index.total_documents == 0:
            return []

        avgdl = self.index.avg_doc_length or 1.0
        scores: Dict[int, float] = {}

        for term in query_terms:
            postings = self.index.get_postings(term)
            if not postings:
                continue

            idf = self._idf(term)
            for doc_id, freq in postings.items():
                doc_len = self.index.doc_lengths.get(doc_id, 1)
                # BM25 term saturation formula
                denom = freq + self.k1 * (1.0 - self.b + self.b * (doc_len / avgdl))
                numerator = freq * (self.k1 + 1.0)
                term_score = idf * (numerator / denom)
                scores[doc_id] = scores.get(doc_id, 0.0) + term_score

        sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]

        return [
            SearchResult(
                doc_id=doc_id,
                score=round(score, 4),
                metadata=self.index.documents.get(doc_id, {})
            )
            for doc_id, score in sorted_docs
        ]
