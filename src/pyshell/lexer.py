"""Shell command tokenizer with quote and redirect handling."""

from __future__ import annotations
import re
from typing import List


class ShellLexer:
    OPERATORS = (">>", "2>&1", "2>", "|", ">", "<", "&")

    def tokenize(self, line: str) -> List[str]:
        tokens: List[str] = []
        i = 0
        n = len(line)

        while i < n:
            # Skip whitespace
            if line[i].isspace():
                i += 1
                continue

            # Check operators
            matched_op = False
            for op in self.OPERATORS:
                if line.startswith(op, i):
                    tokens.append(op)
                    i += len(op)
                    matched_op = True
                    break
            if matched_op:
                continue

            # Word / String token
            word = []
            while i < n and not line[i].isspace():
                # Check if hit operator boundary
                hit_op = False
                for op in self.OPERATORS:
                    if line.startswith(op, i):
                        hit_op = True
                        break
                if hit_op and word:
                    break

                char = line[i]
                if char == "'":
                    # Single quote: consume until closing quote
                    i += 1
                    while i < n and line[i] != "'":
                        word.append(line[i])
                        i += 1
                    if i < n and line[i] == "'":
                        i += 1
                elif char == '"':
                    # Double quote
                    i += 1
                    while i < n and line[i] != '"':
                        if line[i] == "\\" and i + 1 < n:
                            i += 1
                            word.append(line[i])
                        else:
                            word.append(line[i])
                        i += 1
                    if i < n and line[i] == '"':
                        i += 1
                elif char == "\\" and i + 1 < n:
                    i += 1
                    word.append(line[i])
                    i += 1
                else:
                    word.append(char)
                    i += 1

            if word:
                tokens.append("".join(word))

        return tokens
