# PyTransformer: Micro-LLM & Autograd Engine from Scratch in Python

A pure-Python, zero-dependency implementation of a GPT-style Decoder-Only Transformer and scalar Autograd engine inspired by Andrej Karpathy's `micrograd` and `nanoGPT`.

---

## Features

- **Scalar Autograd Engine (`Value`):** Dynamic DAG graph tracing with backpropagation for automatic differentiation (`backward()`).
- **Multi-Head Causal Self-Attention:**
  - Query, Key, Value projections.
  - Scaled dot-product causal attention with lower-triangular masking.
  - Softmax probability normalization.
- **Decoder Block:** Layer normalization, Residual Skip connections, and Feed-Forward Neural Network (MLP with ReLU).
- **Embeddings:** Learned Token Embedding (`wte`) + Learned Positional Embedding (`wpe`).
- **Autoregressive Generation:** Step-by-step next-token sampling loop.

---

## Quickstart Usage

```python
from pytransformer.model import MiniTransformer
from pytransformer.tokenizer import CharacterTokenizer

corpus = "To be, or not to be, that is the question."
tokenizer = CharacterTokenizer(corpus)

model = MiniTransformer(
    vocab_size=tokenizer.vocab_size,
    embed_dim=32,
    num_heads=4,
    context_len=16,
)

prompt = "To be"
input_ids = tokenizer.encode(prompt)
output_ids = model.generate(input_ids, max_new_tokens=10)
print(tokenizer.decode(output_ids))
```

---

## Running Tests

```bash
python -m unittest tests/test_pytransformer.py
```
```
....
----------------------------------------------------------------------
Ran 4 tests in 3.989s

OK
```
