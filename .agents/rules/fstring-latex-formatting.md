---
description: Invariants for embedding LaTeX formulas inside Python f-strings
globs: "**/*.py"
---

# Python f-String LaTeX Invariants

1. **Avoid `\\{` in f-Strings**:
   - In Python 3.12+, backslashes are permitted in f-strings, but `\\{` is interpreted as a line-continuation followed by an unclosed expression brace.
   - Use `\\lbrace` and `\\rbrace` or doubled braces `\\{{ ... \\}}` for literal set notation in LaTeX formulas:
     ```python
     # Correct:
     f"$$\\mathcal{{M}} = \\lbrace \\mathbf{{n}}_1, \\dots, \\mathbf{{n}}_N \\rbrace$$"
     
     # Incorrect (causes SyntaxError: unexpected character after line continuation character):
     f"$$\\mathcal{{M}} = \\{ \\mathbf{{n}}_1, \\dots, \\mathbf{{n}}_N \\}$$"
     ```
