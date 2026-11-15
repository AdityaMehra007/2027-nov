"""Character-level tokenizer for Mini-Transformer."""

from __future__ import annotations
from typing import Dict, List


class CharacterTokenizer:
    def __init__(self, corpus: str) -> None:
        chars = sorted(list(set(corpus)))
        # Ensure space and basic punctuation exist
        for c in " \n\t.,!?":
            if c not in chars:
                chars.append(c)
        chars.sort()

        self.char_to_id: Dict[str, int] = {c: i for i, c in enumerate(chars)}
        self.id_to_char: Dict[int, str] = {i: c for i, c in enumerate(chars)}
        self.vocab_size = len(chars)

    def encode(self, text: str) -> List[int]:
        ids: List[int] = []
        for c in text:
            if c in self.char_to_id:
                ids.append(self.char_to_id[c])
            else:
                # Fallback to space or first token
                ids.append(self.char_to_id.get(" ", 0))
        return ids

    def decode(self, token_ids: List[int]) -> str:
        return "".join([self.id_to_char.get(tid, "") for tid in token_ids])
