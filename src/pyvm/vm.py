from typing import List, Dict, Any, Optional
from .opcodes import Opcode, Instruction

class VirtualMachine:
    def __init__(self):
        self.stack: List[Any] = []
        self.call_stack: List[int] = []
        self.variables: Dict[str, Any] = {}
        self.ip: int = 0
        self.output: List[Any] = []

    def get_var(self, name: str) -> Any:
        return self.variables.get(name)

    def set_var(self, name: str, val: Any):
        self.variables[name] = val

    def run(self, bytecode: List[Instruction]) -> Any:
        """Executes a bytecode instruction stream until HALT or EOF."""
        self.ip = 0
        n_instructions = len(bytecode)

        while 0 <= self.ip < n_instructions:
            inst = bytecode[self.ip]
            op = inst.opcode
            arg = inst.arg

            if op == Opcode.HALT:
                break

            elif op == Opcode.PUSH_CONST:
                self.stack.append(arg)
                self.ip += 1

            elif op == Opcode.POP:
                if not self.stack:
                    raise IndexError("Stack underflow on POP")
                self.stack.pop()
                self.ip += 1

            elif op == Opcode.DUP:
                if not self.stack:
                    raise IndexError("Stack underflow on DUP")
                self.stack.append(self.stack[-1])
                self.ip += 1

            elif op == Opcode.ADD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                self.ip += 1

            elif op == Opcode.SUB:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                self.ip += 1

            elif op == Opcode.MUL:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                self.ip += 1

            elif op == Opcode.DIV:
                b = self.stack.pop()
                a = self.stack.pop()
                if b == 0:
                    raise ZeroDivisionError("Division by zero in VM")
                self.stack.append(a // b if isinstance(a, int) and isinstance(b, int) and a % b == 0 else a / b)
                self.ip += 1

            elif op == Opcode.MOD:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a % b)
                self.ip += 1

            elif op == Opcode.NEG:
                a = self.stack.pop()
                self.stack.append(-a)
                self.ip += 1

            elif op == Opcode.EQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a == b)
                self.ip += 1

            elif op == Opcode.NEQ:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a != b)
                self.ip += 1

            elif op == Opcode.LT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a < b)
                self.ip += 1

            elif op == Opcode.LTE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a <= b)
                self.ip += 1

            elif op == Opcode.GT:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a > b)
                self.ip += 1

            elif op == Opcode.GTE:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a >= b)
                self.ip += 1

            elif op == Opcode.NOT:
                a = self.stack.pop()
                self.stack.append(not a)
                self.ip += 1

            elif op == Opcode.STORE_VAR:
                val = self.stack.pop()
                self.variables[arg] = val
                self.ip += 1

            elif op == Opcode.LOAD_VAR:
                if arg not in self.variables:
                    raise NameError(f"Undefined variable: {arg}")
                self.stack.append(self.variables[arg])
                self.ip += 1

            elif op == Opcode.JUMP:
                self.ip = int(arg)

            elif op == Opcode.JUMP_IF_TRUE:
                cond = self.stack.pop()
                if cond:
                    self.ip = int(arg)
                else:
                    self.ip += 1

            elif op == Opcode.JUMP_IF_FALSE:
                cond = self.stack.pop()
                if not cond:
                    self.ip = int(arg)
                else:
                    self.ip += 1

            elif op == Opcode.CALL:
                self.call_stack.append(self.ip + 1)
                self.ip = int(arg)

            elif op == Opcode.RET:
                if not self.call_stack:
                    raise RuntimeError("Call stack underflow on RET")
                self.ip = self.call_stack.pop()

            elif op == Opcode.PRINT:
                val = self.stack.pop()
                self.output.append(val)
                self.ip += 1

            else:
                raise ValueError(f"Unknown opcode: {op}")

        return self.stack[-1] if self.stack else None
