// File: src/reversible_2085/fredkin_toffoli_adiabatic.hpp
// Zero-Entropy-Dissipation Reversible Logic Synthesis (Toffoli CCNOT & Fredkin CSWAP)
// Every gate is its own unitary inverse (U * U = I), preserving Shannon/von Neumann entropy S = 0.

#pragma once
#include <tuple>
#include <cstdint>
#include <cassert>

namespace Omniverse2126::ReversibleCompute {

    /// Universal Reversible Toffoli Gate (CCNOT): (a, b, c) -> (a, b, c XOR (a AND b))
    [[nodiscard]] constexpr std::tuple<bool, bool, bool> toffoli_gate(bool a, bool b, bool c) noexcept {
        return { a, b, c ^ (a && b) };
    }

    /// Universal Reversible Conservative Fredkin Gate (CSWAP):
    /// Conserves Hamming weight (# of 1s in input == # of 1s in output!)
    [[nodiscard]] constexpr std::tuple<bool, bool, bool> fredkin_gate(bool c, bool p, bool q) noexcept {
        if (c) {
            return { c, q, p };
        }
        return { c, p, q };
    }

    /// 1-Bit Reversible Full Adder using two Toffoli gates and two CNOT gates
    /// Inputs: (a, b, carry_in, ancilla_0 = 0) -> Outputs: (a, a^b, sum, carry_out)
    /// Zero bits are erased; the exact input state can be recovered by running the gates in reverse!
    [[nodiscard]] constexpr std::tuple<bool, bool, bool, bool> reversible_full_adder(
        bool a, bool b, bool c_in
    ) noexcept {
        // Step 1: Toffoli(a, b, 0) -> g1 = a & b
        auto [a1, b1, g1] = toffoli_gate(a, b, false);
        // Step 2: CNOT(a1, b1) -> p1 = a ^ b
        bool p1 = a1 ^ b1;
        // Step 3: Toffoli(p1, c_in, g1) -> c_out = (a & b) ^ ((a ^ b) & c_in)
        auto [p2, c1, c_out] = toffoli_gate(p1, c_in, g1);
        // Step 4: CNOT(p2, c1) -> sum = a ^ b ^ c_in
        bool sum = p2 ^ c1;
        return { a1, p2, sum, c_out };
    }

} // namespace Omniverse2126::ReversibleCompute
