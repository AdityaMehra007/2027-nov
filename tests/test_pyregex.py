import pytest
from src.pyregex.matcher import match, search
from src.pyregex.parser import to_postfix, insert_explicit_concat
from src.pyregex.compiler import compile_regex

def test_explicit_concat_and_postfix():
    # Insert explicit concat
    assert insert_explicit_concat("ab") == "a.b"
    assert insert_explicit_concat("a(b|c)") == "a.(b|c)"
    assert insert_explicit_concat("a*b") == "a*.b"
    assert insert_explicit_concat("a+b") == "a+.b"
    assert insert_explicit_concat("a?b") == "a?.b"

    # Postfix conversion
    assert to_postfix("ab") == "ab."
    assert to_postfix("a|b") == "ab|"
    assert to_postfix("(a|b)*c") == "ab|*c."
    assert to_postfix("a+b") == "a+b."

def test_literal_and_concatenation_matching():
    assert match("abc", "abc") is True
    assert match("abc", "ab") is False
    assert match("abc", "abcd") is False
    assert match("abc", "axc") is False
    assert match("hello", "hello") is True

def test_alternation_matching():
    assert match("cat|dog", "cat") is True
    assert match("cat|dog", "dog") is True
    assert match("cat|dog", "cow") is False
    assert match("apple|banana|cherry", "banana") is True
    assert match("apple|banana|cherry", "grape") is False

def test_kleene_star_matching():
    assert match("a*b", "b") is True
    assert match("a*b", "ab") is True
    assert match("a*b", "aaaaab") is True
    assert match("a*b", "a") is False
    assert match("a*b", "aaac") is False

def test_plus_and_question_mark_matching():
    # Plus: one or more
    assert match("a+b", "b") is False
    assert match("a+b", "ab") is True
    assert match("a+b", "aaab") is True

    # Question mark: zero or one
    assert match("colou?r", "color") is True
    assert match("colou?r", "colour") is True
    assert match("colou?r", "colouur") is False

def test_grouping_and_nesting():
    # (ab)+
    assert match("(ab)+", "ab") is True
    assert match("(ab)+", "abab") is True
    assert match("(ab)+", "ababab") is True
    assert match("(ab)+", "aba") is False

    # (a|b)*c
    assert match("(a|b)*c", "c") is True
    assert match("(a|b)*c", "ac") is True
    assert match("(a|b)*c", "bc") is True
    assert match("(a|b)*c", "abac") is True
    assert match("(a|b)*c", "bbbaaac") is True
    assert match("(a|b)*c", "bbbaaad") is False

def test_substring_search():
    assert search("world", "hello world wide web") is True
    assert search("agent", "autonomous agent system") is True
    assert search("mars", "hello world") is False
    assert search("a+b", "xxxaaabyyy") is True
