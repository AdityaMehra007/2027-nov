import pytest
from src.pyvm.opcodes import Opcode, Instruction
from src.pyvm.vm import VirtualMachine
from src.pyvm.assembler import assemble

def test_arithmetic_and_stack_operations():
    # Program: (10 - 2) * 3
    code = [
        Instruction(Opcode.PUSH_CONST, 10),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.SUB),
        Instruction(Opcode.PUSH_CONST, 3),
        Instruction(Opcode.MUL),
        Instruction(Opcode.HALT)
    ]
    vm = VirtualMachine()
    res = vm.run(code)
    assert res == 24
    assert vm.stack == [24]

def test_variable_storage_and_loading():
    # x = 40; y = x + 2
    code = [
        Instruction(Opcode.PUSH_CONST, 40),
        Instruction(Opcode.STORE_VAR, "x"),
        Instruction(Opcode.LOAD_VAR, "x"),
        Instruction(Opcode.PUSH_CONST, 2),
        Instruction(Opcode.ADD),
        Instruction(Opcode.STORE_VAR, "y"),
        Instruction(Opcode.LOAD_VAR, "y"),
        Instruction(Opcode.HALT)
    ]
    vm = VirtualMachine()
    res = vm.run(code)
    assert res == 42
    assert vm.get_var("x") == 40
    assert vm.get_var("y") == 42

def test_comparisons_and_conditional_jump():
    # if 5 > 3 then result = 100 else result = 200
    code = [
        Instruction(Opcode.PUSH_CONST, 5),
        Instruction(Opcode.PUSH_CONST, 3),
        Instruction(Opcode.GT),            # True on stack
        Instruction(Opcode.JUMP_IF_FALSE, 7), # jump to else if false
        Instruction(Opcode.PUSH_CONST, 100),
        Instruction(Opcode.JUMP, 8),          # jump to end
        # else: (index 7)
        Instruction(Opcode.PUSH_CONST, 200),
        # end: (index 8)
        Instruction(Opcode.HALT)
    ]
    vm = VirtualMachine()
    res = vm.run(code)
    assert res == 100

def test_loop_factorial():
    # Compute 5! = 120
    # n = 5; acc = 1
    # loop:
    #   if n <= 1 jump end
    #   acc = acc * n
    #   n = n - 1
    #   jump loop
    # end:
    #   load acc; halt
    assembly_source = """
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
    code = assemble(assembly_source)
    vm = VirtualMachine()
    res = vm.run(code)
    assert res == 120
    assert vm.get_var("acc") == 120

def test_function_call_and_return():
    # main:
    #   PUSH 21
    #   CALL DOUBLE_FN
    #   HALT
    # DOUBLE_FN:
    #   PUSH 2
    #   MUL
    #   RET
    assembly_source = """
        PUSH 21
        CALL DOUBLE_FN
        HALT

    DOUBLE_FN:
        PUSH 2
        MUL
        RET
    """
    code = assemble(assembly_source)
    vm = VirtualMachine()
    res = vm.run(code)
    assert res == 42

def test_vm_runtime_errors():
    vm = VirtualMachine()
    # Stack underflow
    with pytest.raises(IndexError):
        vm.run([Instruction(Opcode.ADD)])

    # Division by zero
    with pytest.raises(ZeroDivisionError):
        vm.run([
            Instruction(Opcode.PUSH_CONST, 10),
            Instruction(Opcode.PUSH_CONST, 0),
            Instruction(Opcode.DIV)
        ])
