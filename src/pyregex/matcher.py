from typing import Set, List
from .nfa import State
from .compiler import compile_regex

def epsilon_closure(initial_states: Set[State]) -> Set[State]:
    """Computes the epsilon-closure (all states reachable via empty transitions)."""
    closure = set(initial_states)
    stack = list(initial_states)

    while stack:
        state = stack.pop()
        if state.c is None:
            if state.out1 and state.out1 not in closure:
                closure.add(state.out1)
                stack.append(state.out1)
            if state.out2 and state.out2 not in closure:
                closure.add(state.out2)
                stack.append(state.out2)

    return closure

def step(current_states: Set[State], char: str) -> Set[State]:
    """Transitions from current states consuming a single character."""
    next_states: Set[State] = set()

    for s in current_states:
        if s.c == char and s.out1:
            next_states.add(s.out1)

    return epsilon_closure(next_states)

def match(pattern: str, text: str) -> bool:
    """Evaluates whether the entire text matches the regular expression pattern."""
    start_state = compile_regex(pattern)
    current = epsilon_closure({start_state})

    for char in text:
        current = step(current, char)
        if not current:
            return False

    return any(s.is_match for s in current)

def search(pattern: str, text: str) -> bool:
    """Searches for any occurrence of pattern within text."""
    # Prefix-free matching: scan all substring starting positions
    start_state = compile_regex(pattern)

    for i in range(len(text) + 1):
        sub = text[i:]
        current = epsilon_closure({start_state})
        if any(s.is_match for s in current):
            return True

        for char in sub:
            current = step(current, char)
            if any(s.is_match for s in current):
                return True
            if not current:
                break

    return False
