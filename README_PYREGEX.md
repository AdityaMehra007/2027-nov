# `src/pyregex` - Zero-Dependency Thompson NFA Regular Expression Engine

A complete, mathematically rigorous Regular Expression compiler and matcher built purely with Python's standard library using Thompson's Nondeterministic Finite Automata (NFA) construction. It operates with zero dependencies and without using the Python `re` module.

---

## Theoretical Architecture

```
                  Infix Pattern string (e.g. `(a|b)*c`)
                                    |
                                    v
                     [ Shunting-Yard Parser ]
                     - Explicit Concat Insertion (`a.b`)
                     - Operator Precedence Resolution
                                    |
                                    v
                   Postfix Pattern Expression (`ab|*c.`)
                                    |
                                    v
                 [ Thompson NFA Graph Compiler ]
                 - State Graph Fragment Construction
                 - Epsilon (`ε`) Branching Transitions
                                    |
                                    v
                   Non-Deterministic Finite Automata
                                    |
                                    v
               [ Epsilon-Closure Simulation Matcher ]
               - O(m * n) Time Complexity Guarantees
               - Immunity to ReDoS (Catastrophic Backtracking)
```

---

## Supported Grammar

* **Literals:** Any alphanumeric symbol or token.
* **Concatenation:** Implicit or explicit sequence (`ab` -> `a.b`).
* **Alternation / Union:** `|` (`cat|dog`).
* **Kleene Star:** `*` (`a*` = zero or more).
* **Positive Closure:** `+` (`a+` = one or more).
* **Optional Predicate:** `?` (`colou?r` = zero or one).
* **Grouping & Precedence:** `(...)` with arbitrary depth nesting.

---

## Quickstart Usage

```python
from src.pyregex.matcher import match, search

# Exact pattern matching
assert match("cat|dog", "cat") is True
assert match("(ab)+", "ababab") is True
assert match("colou?r", "color") is True

# Substring scanning
assert search("world", "hello world wide web") is True
assert search("a+b", "xxxaaabyyy") is True
```

---

## Test Suite

```bash
python -m pytest tests/test_pyregex.py -v
```
All 7 test specifications pass with 100% fidelity.
