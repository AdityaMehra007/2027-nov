from typing import Dict, List, Optional, Any
from .tokenizer import tokenize

class InvertedIndex:
    def __init__(self):
        # term -> {doc_id: term_frequency}
        self.postings: Dict[str, Dict[int, int]] = {}
        # doc_id -> total token count
        self.doc_lengths: Dict[int, int] = {}
        # doc_id -> metadata
        self.documents: Dict[int, Dict[str, Any]] = {}

    @property
    def total_documents(self) -> int:
        return len(self.doc_lengths)

    @property
    def avg_doc_length(self) -> float:
        if not self.doc_lengths:
            return 0.0
        return sum(self.doc_lengths.values()) / len(self.doc_lengths)

    def add_document(self, doc_id: int, text: str, metadata: Optional[Dict[str, Any]] = None):
        """Indexes a document and updates posting lists."""
        if doc_id in self.documents:
            self.remove_document(doc_id)

        tokens = tokenize(text)
        self.doc_lengths[doc_id] = len(tokens)
        self.documents[doc_id] = metadata or {}
        self.documents[doc_id]["text"] = text

        for t in tokens:
            if t not in self.postings:
                self.postings[t] = {}
            self.postings[t][doc_id] = self.postings[t].get(doc_id, 0) + 1

    def remove_document(self, doc_id: int):
        """Removes a document from the index and updates inverted postings."""
        if doc_id not in self.documents:
            return

        del self.documents[doc_id]
        if doc_id in self.doc_lengths:
            del self.doc_lengths[doc_id]

        empty_terms = []
        for term, doc_map in self.postings.items():
            if doc_id in doc_map:
                del doc_map[doc_id]
                if not doc_map:
                    empty_terms.append(term)

        for term in empty_terms:
            del self.postings[term]

    def get_postings(self, term: str) -> Dict[int, int]:
        """Returns the {doc_id: frequency} map for a given term."""
        return self.postings.get(term, {})
