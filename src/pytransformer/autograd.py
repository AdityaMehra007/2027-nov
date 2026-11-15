"""Micro-autograd scalar computational graph engine."""

from __future__ import annotations
import math
from typing import Callable, Set, Tuple


class Value:
    def __init__(self, data: float, _children: Tuple[Value, ...] = (), _op: str = "") -> None:
        self.data: float = float(data)
        self.grad: float = 0.0
        self._backward: Callable[[], None] = lambda: None
        self._prev: Set[Value] = set(_children)
        self._op: str = _op

    def __repr__(self) -> str:
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"

    def __add__(self, other: Value | float | int) -> Value:
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += out.grad
            other.grad += out.grad

        out._backward = _backward
        return out

    def __radd__(self, other: Value | float | int) -> Value:
        return self + other

    def __mul__(self, other: Value | float | int) -> Value:
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out

    def __rmul__(self, other: Value | float | int) -> Value:
        return self * other

    def __pow__(self, other: float | int) -> Value:
        assert isinstance(other, (int, float)), "only supporting int/float powers"
        out = Value(self.data**other, (self,), f"**{other}")

        def _backward():
            self.grad += (other * (self.data ** (other - 1))) * out.grad

        out._backward = _backward
        return out

    def __neg__(self) -> Value:
        return self * -1.0

    def __sub__(self, other: Value | float | int) -> Value:
        return self + (-other)

    def __rsub__(self, other: Value | float | int) -> Value:
        return other + (-self)

    def __truediv__(self, other: Value | float | int) -> Value:
        other = other if isinstance(other, Value) else Value(other)
        return self * (other**-1)

    def relu(self) -> Value:
        out = Value(0.0 if self.data < 0 else self.data, (self,), "ReLU")

        def _backward():
            self.grad += (out.data > 0) * out.grad

        out._backward = _backward
        return out

    def exp(self) -> Value:
        out = Value(math.exp(self.data), (self,), "exp")

        def _backward():
            self.grad += out.data * out.grad

        out._backward = _backward
        return out

    def log(self) -> Value:
        out = Value(math.log(max(self.data, 1e-12)), (self,), "log")

        def _backward():
            self.grad += (1.0 / max(self.data, 1e-12)) * out.grad

        out._backward = _backward
        return out

    def backward(self) -> None:
        topo: list[Value] = []
        visited: set[Value] = set()

        def build_topo(v: Value):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)

        build_topo(self)

        self.grad = 1.0
        for node in reversed(topo):
            node._backward()
