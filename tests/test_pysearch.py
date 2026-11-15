import pytest
from src.pysearch.tokenizer import tokenize
from src.pysearch.index import InvertedIndex
from src.pysearch.bm25 import BM25Ranker
from src.pysearch.query import BooleanQueryEngine

def test_tokenizer_normalization_and_stemming():
    text = "The FAST runners are running rapidly in the race!"
    tokens = tokenize(text)
    # Stopwords ('the', 'are', 'in') removed
    assert "the" not in tokens
    assert "are" not in tokens
    assert "in" not in tokens
    # Lowercase & stemmed
    assert "fast" in tokens
    assert "runner" in tokens or "run" in tokens
    assert "race" in tokens

def test_inverted_index_indexing():
    idx = InvertedIndex()
    idx.add_document(1, "Python is a modern high-level programming language", {"title": "Doc1"})
    idx.add_document(2, "Rust is a fast systems programming language", {"title": "Doc2"})

    assert idx.total_documents == 2
    postings = idx.get_postings("program")
    assert 1 in postings
    assert 2 in postings

    # Remove document 1
    idx.remove_document(1)
    assert idx.total_documents == 1
    postings_after = idx.get_postings("program")
    assert 1 not in postings_after
    assert 2 in postings_after

def test_bm25_ranking():
    idx = InvertedIndex()
    idx.add_document(1, "Distributed systems consensus algorithms using Paxos and Raft", {"title": "Consensus Systems"})
    idx.add_document(2, "Quantum computing surface code error correction fidelity", {"title": "Quantum Physics"})
    idx.add_document(3, "High performance consensus algorithms and distributed databases", {"title": "DB Consensus"})

    ranker = BM25Ranker(idx)
    results = ranker.search("distributed consensus", top_k=5)

    assert len(results) > 0
    # Doc 1 and Doc 3 must be at the top
    top_doc_ids = [r.doc_id for r in results]
    assert top_doc_ids[0] in [1, 3]
    assert 2 not in top_doc_ids  # Doc 2 has neither distributed nor consensus

def test_boolean_query_filters():
    idx = InvertedIndex()
    idx.add_document(1, "Apple iPhone smart device mobile phone", {"id": 1})
    idx.add_document(2, "Apple fruit sweet red organic apple tree", {"id": 2})
    idx.add_document(3, "Android Google smart device mobile operating system", {"id": 3})

    engine = BooleanQueryEngine(idx)

    # AND search: 'apple' AND 'smart' -> only Doc 1
    res_and = engine.search_and(["apple", "smart"])
    assert res_and == {1}

    # OR search: 'iphone' OR 'android' -> Doc 1 and Doc 3
    res_or = engine.search_or(["iphone", "android"])
    assert 1 in res_or and 3 in res_or
    assert 2 not in res_or

    # NOT filter: 'apple' NOT 'fruit' -> Doc 1
    res_not = engine.search_not(positive_terms=["apple"], negative_terms=["fruit"])
    assert res_not == {1}

def test_empty_query_and_unknown_terms():
    idx = InvertedIndex()
    idx.add_document(1, "Single document content")
    ranker = BM25Ranker(idx)

    assert ranker.search("") == []
    assert ranker.search("nonexistentgibberishterm") == []
