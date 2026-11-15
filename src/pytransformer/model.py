"""Mini-Transformer neural architecture in pure Python micro-autograd."""

from __future__ import annotations
import math
import random
from typing import List
from pytransformer.autograd import Value


class Linear:
    """Linear layer: y = x @ W^T + b."""

    def __init__(self, in_features: int, out_features: int, bias: bool = True) -> None:
        self.in_features = in_features
        self.out_features = out_features
        # He / Xavier initialization
        scale = math.sqrt(2.0 / (in_features + out_features))
        self.weight: List[List[Value]] = [
            [Value(random.uniform(-scale, scale)) for _ in range(in_features)]
            for _ in range(out_features)
        ]
        self.bias: List[Value] = [Value(0.0) for _ in range(out_features)] if bias else []

    def forward(self, x: List[Value]) -> List[Value]:
        out: List[Value] = []
        for i in range(self.out_features):
            acc: Value = self.bias[i] if self.bias else Value(0.0)
            for j in range(self.in_features):
                acc = acc + (self.weight[i][j] * x[j])
            out.append(acc)
        return out

    def __call__(self, x: List[Value]) -> List[Value]:
        return self.forward(x)

    def parameters(self) -> List[Value]:
        params = [w for row in self.weight for w in row]
        if self.bias:
            params.extend(self.bias)
        return params


class MultiHeadAttention:
    """Multi-Head Self-Attention using pure Value scalars."""

    def __init__(self, embed_dim: int, num_heads: int) -> None:
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = max(1, embed_dim // num_heads)

        self.q_proj = Linear(embed_dim, embed_dim)
        self.k_proj = Linear(embed_dim, embed_dim)
        self.v_proj = Linear(embed_dim, embed_dim)
        self.out_proj = Linear(embed_dim, embed_dim)

    def forward(self, x_seq: List[List[Value]]) -> List[List[Value]]:
        seq_len = len(x_seq)
        if seq_len == 0:
            return []

        # Project Q, K, V for each token in the sequence
        q_seq = [self.q_proj.forward(x) for x in x_seq]
        k_seq = [self.k_proj.forward(x) for x in x_seq]
        v_seq = [self.v_proj.forward(x) for x in x_seq]

        out_seq: List[List[Value]] = []
        scale = 1.0 / math.sqrt(self.embed_dim)

        # Simplified causal self-attention over sequence
        for t in range(seq_len):
            # Compute attention scores against preceding tokens (causal)
            scores: List[Value] = []
            for s in range(t + 1):
                # Dot product q[t] . k[s]
                dot = Value(0.0)
                for d in range(self.embed_dim):
                    dot = dot + (q_seq[t][d] * k_seq[s][d])
                scores.append(dot * scale)

            # Softmax
            exp_scores = [s.exp() for s in scores]
            sum_exp = Value(0.0)
            for es in exp_scores:
                sum_exp = sum_exp + es
            attn_weights = [es / sum_exp for es in exp_scores]

            # Weighted sum of values
            context_t: List[Value] = [Value(0.0) for _ in range(self.embed_dim)]
            for s in range(t + 1):
                w = attn_weights[s]
                for d in range(self.embed_dim):
                    context_t[d] = context_t[d] + (w * v_seq[s][d])

            # Output projection
            out_t = self.out_proj.forward(context_t)
            out_seq.append(out_t)

        return out_seq

    def parameters(self) -> List[Value]:
        return (
            self.q_proj.parameters()
            + self.k_proj.parameters()
            + self.v_proj.parameters()
            + self.out_proj.parameters()
        )


class MiniTransformer:
    """Decoder-only autoregressive Transformer with character embeddings and causal attention."""

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int = 16,
        num_heads: int = 2,
        context_len: int = 8,
    ) -> None:
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.context_len = context_len

        # Token embedding lookup table
        scale = math.sqrt(1.0 / embed_dim)
        self.token_embeddings: List[List[Value]] = [
            [Value(random.uniform(-scale, scale)) for _ in range(embed_dim)]
            for _ in range(vocab_size)
        ]

        # Learnable positional embeddings
        self.pos_embeddings: List[List[Value]] = [
            [Value(random.uniform(-scale, scale)) for _ in range(embed_dim)]
            for _ in range(context_len)
        ]

        self.mha = MultiHeadAttention(embed_dim, num_heads)
        self.ffn1 = Linear(embed_dim, embed_dim * 2)
        self.ffn2 = Linear(embed_dim * 2, embed_dim)
        self.lm_head = Linear(embed_dim, vocab_size)

    def forward(self, input_ids: List[int]) -> List[List[Value]]:
        # Truncate to context length
        tokens = input_ids[-self.context_len:]
        seq_len = len(tokens)
        if seq_len == 0:
            return []

        # Embed tokens and add positional encodings
        x_seq: List[List[Value]] = []
        for pos, tid in enumerate(tokens):
            safe_tid = tid % self.vocab_size
            tok_emb = self.token_embeddings[safe_tid]
            pos_emb = self.pos_embeddings[pos % self.context_len]
            x_seq.append([tok_emb[d] + pos_emb[d] for d in range(self.embed_dim)])

        # Transformer Block: Self-Attention + Residual
        attn_out = self.mha.forward(x_seq)
        h_seq: List[List[Value]] = []
        for t in range(seq_len):
            h_seq.append([x_seq[t][d] + attn_out[t][d] for d in range(self.embed_dim)])

        # Feed-Forward Network + Residual
        logits_seq: List[List[Value]] = []
        for t in range(seq_len):
            ffn_hidden = [v.relu() for v in self.ffn1.forward(h_seq[t])]
            ffn_out = self.ffn2.forward(ffn_hidden)
            final_h = [h_seq[t][d] + ffn_out[d] for d in range(self.embed_dim)]
            logits = self.lm_head.forward(final_h)
            logits_seq.append(logits)

        return logits_seq

    def generate(self, input_ids: List[int], max_new_tokens: int = 5) -> List[int]:
        tokens = list(input_ids)
        for _ in range(max_new_tokens):
            logits_seq = self.forward(tokens)
            if not logits_seq:
                tokens.append(0)
                continue
            last_logits = logits_seq[-1]
            next_token = max(range(self.vocab_size), key=lambda i: last_logits[i].data)
            tokens.append(next_token)
        return tokens

    def parameters(self) -> List[Value]:
        params: List[Value] = [v for row in self.token_embeddings for v in row]
        params.extend([v for row in self.pos_embeddings for v in row])
        params.extend(self.mha.parameters())
        params.extend(self.ffn1.parameters())
        params.extend(self.ffn2.parameters())
        params.extend(self.lm_head.parameters())
        return params
