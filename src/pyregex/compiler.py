from typing import List
from .nfa import State, Fragment
from .parser import to_postfix

def compile_regex(regex: str) -> State:
    """Compiles a regular expression into an NFA using Thompson's construction."""
    if not regex:
        # Match empty string
        s = State()
        s.is_match = True
        return s

    postfix = to_postfix(regex)
    stack: List[Fragment] = []

    for c in postfix:
        if c == '.':
            # Concatenation
            if len(stack) < 2:
                continue
            frag2 = stack.pop()
            frag1 = stack.pop()
            frag1.patch(frag2.start)
            stack.append(Fragment(frag1.start, frag2.dangling_outs))

        elif c == '|':
            # Alternation
            if len(stack) < 2:
                continue
            frag2 = stack.pop()
            frag1 = stack.pop()
            s = State(c=None, out1=frag1.start, out2=frag2.start)
            stack.append(Fragment(s, frag1.dangling_outs + frag2.dangling_outs))

        elif c == '*':
            # Zero or more
            if not stack:
                continue
            frag = stack.pop()
            s = State(c=None, out1=frag.start, out2=None)
            frag.patch(s)
            stack.append(Fragment(s, [(s, 2)]))

        elif c == '+':
            # One or more
            if not stack:
                continue
            frag = stack.pop()
            s = State(c=None, out1=frag.start, out2=None)
            frag.patch(s)
            stack.append(Fragment(frag.start, [(s, 2)]))

        elif c == '?':
            # Zero or one
            if not stack:
                continue
            frag = stack.pop()
            s = State(c=None, out1=frag.start, out2=None)
            stack.append(Fragment(s, frag.dangling_outs + [(s, 2)]))

        else:
            # Literal character
            s = State(c=c)
            stack.append(Fragment(s, [(s, 1)]))

    if not stack:
        s = State()
        s.is_match = True
        return s

    final_frag = stack.pop()
    match_state = State()
    match_state.is_match = True
    final_frag.patch(match_state)

    return final_frag.start
