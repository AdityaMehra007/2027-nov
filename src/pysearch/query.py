from typing import List, Set
from .index import InvertedIndex
from .tokenizer import tokenize

class BooleanQueryEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def _get_doc_ids_for_term(self, term: str) -> Set[int]:
        tokens = tokenize(term)
        if not tokens:
            return set()
        # Union over any tokens generated from term string
        docs: Set[int] = set()
        for t in tokens:
            docs.update(self.index.get_postings(t).keys())
        return docs

    def search_and(self, terms: List[str]) -> Set[int]:
        """Returns documents that match ALL specified terms."""
        if not terms:
            return set()

        result: Set[int] = set()
        first = True

        for term in terms:
            matching = self._get_doc_ids_for_term(term)
            if first:
                result = matching
                first = False
            else:
                result = result.intersection(matching)

            if not result:
                break

        return result

    def search_or(self, terms: List[str]) -> Set[int]:
        """Returns documents that match AT LEAST ONE specified term."""
        result: Set[int] = set()
        for term in terms:
            result.update(self._get_doc_ids_for_term(term))
        return result

    def search_not(self, positive_terms: List[str], negative_terms: List[str]) -> Set[int]:
        """Returns documents that match positive terms while excluding negative terms."""
        positive_docs = self.search_or(positive_terms) if positive_terms else set(self.index.documents.keys())
        negative_docs = self.search_or(negative_terms) if negative_terms else set()
        return positive_docs - negative_docs
