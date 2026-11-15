import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Tuple, Any


class CompressionMode(str, Enum):
    PASSTHROUGH = "PASSTHROUGH"
    LIGHT = "LIGHT"
    CAVEMAN = "CAVEMAN"
    AGGRESSIVE = "AGGRESSIVE"


@dataclass
class CompressionStats:
    original_chars: int
    compressed_chars: int
    original_tokens_est: int
    compressed_tokens_est: int
    reduction_ratio: float
    mode: CompressionMode


class PromptCompressor:
    """
    Zero-dependency prompt & context compressor inspired by RTK and Caveman.
    Reduces token consumption across high-throughput agent loops while strictly
    preserving technical semantics, code blocks, parameters, and instruction constraints.
    """

    # Filler phrases that add zero informational entropy to LLM reasoning
    FILLER_PATTERNS = [
        re.compile(r"\b(?:could|would|can)\s+you\s+(?:please\s+)?(?:kindly\s+)?", re.IGNORECASE),
        re.compile(r"\bplease\s+(?:make\s+sure\s+to\s+|be\s+sure\s+to\s+)?", re.IGNORECASE),
        re.compile(r"\bkindly\s+", re.IGNORECASE),
        re.compile(r"\bi\s+(?:would\s+like|want)\s+you\s+to\s+", re.IGNORECASE),
        re.compile(r"\bin\s+order\s+to\s+", re.IGNORECASE),
        re.compile(r"\bas\s+a\s+matter\s+of\s+fact,?\s*", re.IGNORECASE),
        re.compile(r"\bat\s+the\s+end\s+of\s+the\s+day,?\s*", re.IGNORECASE),
        re.compile(r"\bfor\s+the\s+purpose\s+of\s+", re.IGNORECASE),
        re.compile(r"\bthank(?:s|\s+you)(?:\s+in\s+advance)?(?:!|\.|\,)?\s*", re.IGNORECASE),
        re.compile(r"\b(?:hello|hi|hey|greetings)(?:\s+there)?(?:!|\.|\,)?\s*", re.IGNORECASE),
        re.compile(r"\bi\s+hope\s+this\s+helps(?:\.|\!)?\s*", re.IGNORECASE),
    ]

    ORPHAN_LEADING_PUNCTUATION = re.compile(r"^\s*[\!\.\,\:\;]+\s*", re.MULTILINE)

    MULTIPLE_SPACES = re.compile(r"[ \t]+")
    MULTIPLE_NEWLINES = re.compile(r"\n{3,}")
    CODE_BLOCK_PATTERN = re.compile(r"(```[\s\S]*?```|`[^`\n]+`)")

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Estimate token count based on words and characters (approx 1 token ~ 4 chars)."""
        if not text:
            return 0
        words = len(text.split())
        chars = len(text)
        return max(1, (words + chars // 4) // 2)

    def compress_text(self, text: str, mode: CompressionMode = CompressionMode.CAVEMAN) -> Tuple[str, CompressionStats]:
        """Compresses a text prompt according to the selected compression mode."""
        if mode == CompressionMode.PASSTHROUGH or not text:
            tokens = self._estimate_tokens(text)
            stats = CompressionStats(
                original_chars=len(text),
                compressed_chars=len(text),
                original_tokens_est=tokens,
                compressed_tokens_est=tokens,
                reduction_ratio=0.0,
                mode=mode,
            )
            return text, stats

        orig_len = len(text)
        orig_tokens = self._estimate_tokens(text)

        # Protect code blocks from modification
        code_blocks: List[str] = []
        def _extract_code(match):
            idx = len(code_blocks)
            code_blocks.append(match.group(0))
            return f"__CODE_BLOCK_{idx}__"

        processed = self.CODE_BLOCK_PATTERN.sub(_extract_code, text)

        # Stage 1: Light Compression (normalize whitespace)
        processed = self.MULTIPLE_SPACES.sub(" ", processed)
        processed = "\n".join(line.strip() for line in processed.splitlines())
        processed = self.MULTIPLE_NEWLINES.sub("\n\n", processed)

        # Stage 2: Caveman / Aggressive Compression
        if mode in (CompressionMode.CAVEMAN, CompressionMode.AGGRESSIVE):
            for pattern in self.FILLER_PATTERNS:
                processed = pattern.sub("", processed)

            # Re-normalize spacing and strip orphan leading punctuation post-removal
            processed = self.ORPHAN_LEADING_PUNCTUATION.sub("", processed)
            processed = self.MULTIPLE_SPACES.sub(" ", processed)
            processed = "\n".join(line.strip() for line in processed.splitlines() if line.strip())

        if mode == CompressionMode.AGGRESSIVE:
            # Aggressive shorthand compression on common phrases
            processed = re.sub(r"\bwith\s+respect\s+to\b", "w.r.t.", processed, flags=re.IGNORECASE)
            processed = re.sub(r"\bas\s+soon\s+as\s+possible\b", "ASAP", processed, flags=re.IGNORECASE)
            processed = re.sub(r"\bfor\s+example\b", "e.g.", processed, flags=re.IGNORECASE)
            processed = re.sub(r"\bthat\s+is\s+to\s+say\b", "i.e.", processed, flags=re.IGNORECASE)

        # Restore code blocks verbatim
        for idx, block in enumerate(code_blocks):
            processed = processed.replace(f"__CODE_BLOCK_{idx}__", block)

        compressed_len = len(processed)
        compressed_tokens = self._estimate_tokens(processed)
        reduction = max(0.0, (orig_tokens - compressed_tokens) / orig_tokens) if orig_tokens > 0 else 0.0

        stats = CompressionStats(
            original_chars=orig_len,
            compressed_chars=compressed_len,
            original_tokens_est=orig_tokens,
            compressed_tokens_est=compressed_tokens,
            reduction_ratio=round(reduction, 4),
            mode=mode,
        )
        return processed, stats

    def compress_messages(
        self,
        messages: List[Dict[str, Any]],
        mode: CompressionMode = CompressionMode.CAVEMAN,
    ) -> Tuple[List[Dict[str, Any]], CompressionStats]:
        """Compresses a list of OpenAI/Anthropic format chat messages."""
        compressed_messages: List[Dict[str, Any]] = []
        total_orig_chars = 0
        total_comp_chars = 0
        total_orig_toks = 0
        total_comp_toks = 0

        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str) and content:
                comp_text, stats = self.compress_text(content, mode=mode)
                new_msg = dict(msg)
                new_msg["content"] = comp_text
                compressed_messages.append(new_msg)

                total_orig_chars += stats.original_chars
                total_comp_chars += stats.compressed_chars
                total_orig_toks += stats.original_tokens_est
                total_comp_toks += stats.compressed_tokens_est
            else:
                compressed_messages.append(msg)

        reduction = (
            max(0.0, (total_orig_toks - total_comp_toks) / total_orig_toks)
            if total_orig_toks > 0
            else 0.0
        )

        overall_stats = CompressionStats(
            original_chars=total_orig_chars,
            compressed_chars=total_comp_chars,
            original_tokens_est=total_orig_toks,
            compressed_tokens_est=total_comp_toks,
            reduction_ratio=round(reduction, 4),
            mode=mode,
        )
        return compressed_messages, overall_stats
