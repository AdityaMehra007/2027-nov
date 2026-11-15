# PyTransformer: Generative Transformer from Scratch in Pure Python

A complete, zero-dependency implementation of a Generative Pre-trained Transformer (GPT) and scalar computational graph autograd engine built entirely in the Python standard library.

PyTransformer demonstrates the exact mechanics of modern Large Language Models: scalar reverse-mode automatic differentiation, multi-head causal self-attention, learned positional encodings, feed-forward layers, and autoregressive text generation.

---

## Architecture Overview

```
                      Raw Text / Prompt
                             |
                             v
                  [ CharacterTokenizer ]
                             |
                     token_ids (List[int])
                             |
                             v
                 [ Embedding + PosEnc ]
                             |
                   x_seq (List[List[Value]])
                             |
                             v
              +------------------------------+
              |      MiniTransformer         |
              |                              |
              |  +------------------------+  |
              |  | MultiHeadAttention     |  |
              |  | - Q, K, V Projections  |  |
              |  | - Causal Attention Mask|  |
              |  | - Softmax via Value.exp|  |
              |  +------------------------+  |
              |               |              |
              |         Residual Add         |
              |               |              |
              |  +------------------------+  |
              |  | FeedForward Network    |  |
              |  | - Linear -> ReLU -> Lin|  |
              |  +------------------------+  |
              |               |              |
              |         Residual Add         |
              |               |              |
              |  +------------------------+  |
              |  | Language Modeling Head |  |
              |  | - Linear (embed->vocab)|  |
              |  +------------------------+  |
              +------------------------------+
                             |
                     logits_seq
                             |
                             v
             Autoregressive Next-Token Sampling
```

---

## Core Components

### 1. Scalar Micro-Autograd (`autograd.py`)
- `Value(data)`: Encapsulates scalar values with computational graph history (`_prev`), tracking gradients (`grad`) and backprop closures (`_backward`).
- Supported operations: `+`, `-`, `*`, `/`, `**` (power), `relu()`, `exp()`, `log()`.
- Topological sort DAG resolution in `backward()`.

### 2. Neural Building Blocks (`model.py`)
- `Linear`: Computes affine transformations $y = x W^T + b$ using Value scalar arithmetic.
- `MultiHeadAttention`: Computes causal scaled dot-product self-attention with proper scaling and scalar softmax.
- `MiniTransformer`: Full decoder-only architecture with token embeddings, learnable positional encodings, self-attention, and projection head.
- `generate(input_ids, max_new_tokens)`: Autoregressive token generation loop.

### 3. Tokenizer (`tokenizer.py`)
- `CharacterTokenizer`: Deterministic bidirectional vocabulary mapping for arbitrary character sets and natural language text.

---

## Testing & Verification

Run the verification suite:
```bash
pytest tests/test_pytransformer.py -v
```

All 4 test cases verify:
1. Reverse-mode scalar backpropagation with exact analytical derivative matching.
2. Linear layer forward pass dimensionality and autograd connectivity.
3. Character tokenizer bijection and roundtrip lossless encoding/decoding.
4. Full causal attention forward pass and autoregressive generative sampling.
