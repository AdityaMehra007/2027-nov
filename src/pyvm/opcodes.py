from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Optional

class Opcode(Enum):
    # Stack Operations
    PUSH_CONST = "PUSH"
    POP = "POP"
    DUP = "DUP"

    # Arithmetic
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    NEG = "NEG"

    # Logic & Comparisons
    EQ = "EQ"
    NEQ = "NEQ"
    LT = "LT"
    LTE = "LTE"
    GT = "GT"
    GTE = "GTE"
    NOT = "NOT"

    # Variable Binding
    STORE_VAR = "STORE"
    LOAD_VAR = "LOAD"

    # Control Flow
    JUMP = "JUMP"
    JUMP_IF_TRUE = "JUMP_IF_TRUE"
    JUMP_IF_FALSE = "JUMP_IF_FALSE"

    # Functions
    CALL = "CALL"
    RET = "RET"

    # System
    PRINT = "PRINT"
    HALT = "HALT"

@dataclass
class Instruction:
    opcode: Opcode
    arg: Any = None
