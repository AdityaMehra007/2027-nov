# `src/pyvm` - Zero-Dependency Stack Virtual Machine and Bytecode Assembler

A clean, high-performance stack-based virtual machine and multi-pass assembler implemented purely in the Python standard library.

## Architecture & Features

1. **Instruction Set Architecture (`src/pyvm/opcodes.py`)**:
   - **Stack Opcodes**: `PUSH`, `POP`, `DUP`.
   - **Arithmetic & Modulo**: `ADD`, `SUB`, `MUL`, `DIV`, `MOD`, `NEG`.
   - **Comparison & Logic**: `EQ`, `NEQ`, `LT`, `LTE`, `GT`, `GTE`, `NOT`.
   - **Variable Scoping**: `STORE`, `LOAD`.
   - **Control Flow**: `JUMP`, `JUMP_IF_TRUE`, `JUMP_IF_FALSE`.
   - **Subroutines**: `CALL`, `RET` with automated return address call frames.
   - **System Controls**: `PRINT`, `HALT`.

2. **Virtual Machine Engine (`src/pyvm/vm.py`)**:
   - Instruction pointer (`ip`) evaluation loop.
   - Dedicated operand evaluation stack and return address call stack.
   - Local/global variable environment bindings.
   - Runtime fault traps (stack underflow, division-by-zero, undefined symbols).

3. **Symbolic Assembler (`src/pyvm/assembler.py`)**:
   - Two-pass assembler parsing human-readable assembly syntax with comment stripping (`#`).
   - Symbolic label resolution for jump destinations and function entry points.
   - Automatic literal parsing for integers, floats, and strings.

## Test Suite

```bash
python -m pytest tests/test_pyvm.py -v
```
All 6 test specifications pass with 100% fidelity.
