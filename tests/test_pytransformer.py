import math
import unittest
from pytransformer.autograd import Value
from pytransformer.model import Linear, MultiHeadAttention, MiniTransformer
from pytransformer.tokenizer import CharacterTokenizer

class TestPyTransformer(unittest.TestCase):
    def test_autograd_scalar_backprop(self):
        # f(x, y) = (x * 2 + y)^2
        x = Value(3.0)
        y = Value(-1.0)
        z = (x * 2.0 + y) ** 2  # (6 - 1)^2 = 25
        z.backward()

        self.assertEqual(z.data, 25.0)
        # dz/dx = 2 * (x * 2 + y) * 2 = 2 * 5 * 2 = 20
        self.assertEqual(x.grad, 20.0)
        # dz/dy = 2 * (x * 2 + y) * 1 = 10
        self.assertEqual(y.grad, 10.0)

    def test_linear_layer_forward(self):
        layer = Linear(in_features=3, out_features=2)
        x = [Value(1.0), Value(2.0), Value(3.0)]
        out = layer.forward(x)
        self.assertEqual(len(out), 2)
        # Verify scalar outputs
        self.assertIsInstance(out[0], Value)

    def test_tokenizer_encode_decode(self):
        corpus = "abcdefghijklmnopqrstuvwxyz 0123456789"
        tok = CharacterTokenizer(corpus)
        text = "hello world"
        encoded = tok.encode(text)
        decoded = tok.decode(encoded)
        self.assertEqual(decoded, text)

    def test_transformer_forward_and_generate(self):
        corpus = "hello world"
        tok = CharacterTokenizer(corpus)
        model = MiniTransformer(
            vocab_size=tok.vocab_size,
            embed_dim=16,
            num_heads=2,
            context_len=8,
        )

        input_ids = tok.encode("hello")
        logits = model.forward(input_ids)
        # Logits should have shape [len(input_ids), vocab_size]
        self.assertEqual(len(logits), len(input_ids))
        self.assertEqual(len(logits[-1]), tok.vocab_size)

        # Autoregressive generation
        generated = model.generate(input_ids, max_new_tokens=5)
        self.assertEqual(len(generated), len(input_ids) + 5)

if __name__ == "__main__":
    unittest.main()
