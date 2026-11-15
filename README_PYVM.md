# `src/pyvm` - Zero-Dependency Stack-Based Bytecode Virtual Machine & Assembler

A complete, high-performance stack-based Bytecode Virtual Machine and two-pass Assembler implemented purely with Python 3.13 standard library (`enum`, `dataclasses`, `typing`).

---

## Architecture & Components

```
                Assembly Source Code (.asm)
                            |
                            v
               [ Two-Pass Assembler ]
               - Pass 1: Symbol Table & Label Offsets
               - Pass 2: Opcode & Operand Resolution
                            |
                            v
              Bytecode Instruction Stream
                            |
                            v
               [ Virtual Machine Core ]
               - Call Stack & Execution Frames
               - Data Stack (LIFO Evaluation)
               - Lexical Environment / Variables
               - Instruction Pointer (IP) Engine
                            |
                            v
                     Computed Result
```

### 1. Instruction Set Architecture (`src/pyvm/opcodes.py`)
* **Stack & Constant Manipulation:** `PUSH_CONST`, `POP`, `DUP`
* **Arithmetic Operations:** `ADD`, `SUB`, `MUL`, `DIV`, `MOD`
* **Logical & Comparison Predicates:** `EQ`, `NEQ`, `LT`, `LTE`, `GT`, `GTE`
* **Variable Storage & Loading:** `STORE_VAR`, `LOAD_VAR`
* **Control Flow & Branching:** `JUMP`, `JUMP_IF_TRUE`, `JUMP_IF_FALSE`
* **Subroutine & Frame Management:** `CALL`, `RET`
* **Execution Boundary:** `HALT`

### 2. Two-Pass Symbolic Assembler (`src/pyvm/assembler.py`)
* **Pass 1:** Strips comments, parses labels (`LABEL:`), and maps target instruction pointers into a deterministic symbol table.
* **Pass 2:** Resolves mnemonic operations and binds symbolic target branch labels to absolute instruction offsets.

### 3. Virtual Machine Runtime (`src/pyvm/vm.py`)
* **Evaluation Stack:** Fast LIFO data stack supporting arithmetic and boolean logic.
* **Call Stack:** Frame-based call return stack enabling re-entrant subroutines and recursion.
* **Error Handling:** Graceful trapped exceptions for stack underflow and division by zero.

---

## Quickstart Usage

```python
from src.pyvm.assembler import assemble
from src.pyvm.vm import VirtualMachine

# Factorial of 5 (5! = 120)
assembly_code = """
    PUSH 5
    STORE n
    PUSH 1
    STORE acc

LOOP:
    LOAD n
    PUSH 1
    LTE
    JUMP_IF_TRUE END

    LOAD acc
    LOAD n
    MUL
    STORE acc

    LOAD n
    PUSH 1
    SUB
    STORE n

    JUMP LOOP

END:
    LOAD acc
    HALT
"""

instructions = assemble(assembly_code)
vm = VirtualMachine()
result = vm.run(instructions)
print(f"Computed 5! = {result}")  # 120
```

---

## Test Suite

```bash
pytest tests/test_pyvm.py -v
```
All 6 test specifications pass with 100% fidelity.
