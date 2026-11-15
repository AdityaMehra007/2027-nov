import re
from typing import List, Dict, Any
from .opcodes import Opcode, Instruction

def parse_literal(val_str: str) -> Any:
    """Parses a string token into int, float, or string."""
    try:
        return int(val_str)
    except ValueError:
        pass
    try:
        return float(val_str)
    except ValueError:
        pass
    if (val_str.startswith('"') and val_str.endswith('"')) or (val_str.startswith("'") and val_str.endswith("'")):
        return val_str[1:-1]
    return val_str

def assemble(source: str) -> List[Instruction]:
    """Compiles assembly source text with symbolic labels into a list of Instructions."""
    lines = source.strip().splitlines()

    # Pass 1: Collect labels and strip comments/empty lines
    cleaned_lines = []
    labels: Dict[str, int] = {}

    for raw in lines:
        line = re.sub(r'#.*$', '', raw).strip()
        if not line:
            continue

        if line.endswith(":"):
            label_name = line[:-1].strip()
            labels[label_name] = len(cleaned_lines)
            continue

        # Check if line has label prefix: LABEL: INSTRUCTION ...
        label_match = re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if label_match:
            label_name = label_match.group(1).strip()
            rest = label_match.group(2).strip()
            labels[label_name] = len(cleaned_lines)
            if rest:
                cleaned_lines.append(rest)
            continue

        cleaned_lines.append(line)

    # Pass 2: Emit instructions and resolve label targets
    instructions: List[Instruction] = []
    op_map = {op.value: op for op in Opcode}

    for line in cleaned_lines:
        tokens = line.split(maxsplit=1)
        mnemonic = tokens[0].upper()
        arg_str = tokens[1].strip() if len(tokens) > 1 else None

        if mnemonic not in op_map:
            raise ValueError(f"Unrecognized opcode mnemonic: {mnemonic}")

        opcode = op_map[mnemonic]
        arg = None

        if arg_str is not None:
            if opcode in (Opcode.JUMP, Opcode.JUMP_IF_TRUE, Opcode.JUMP_IF_FALSE, Opcode.CALL):
                # Resolve label or direct int
                if arg_str in labels:
                    arg = labels[arg_str]
                else:
                    arg = parse_literal(arg_str)
            else:
                arg = parse_literal(arg_str)

        instructions.append(Instruction(opcode=opcode, arg=arg))

    return instructions
