from typing import Optional, List, Tuple

class State:
    _id_counter = 0

    def __init__(self, c: Optional[str] = None, out1: Optional['State'] = None, out2: Optional['State'] = None):
        State._id_counter += 1
        self.id = State._id_counter
        self.c = c                  # None means epsilon transition
        self.out1 = out1
        self.out2 = out2
        self.is_match = False

    def __repr__(self):
        return f"<State {self.id} c={self.c} match={self.is_match}>"

class Fragment:
    def __init__(self, start: State, dangling_outs: List[Tuple[State, int]]):
        self.start = start
        # Each item is (state, 1) or (state, 2) representing state.out1 or state.out2
        self.dangling_outs = dangling_outs

    def patch(self, target: State):
        for state, out_idx in self.dangling_outs:
            if out_idx == 1:
                state.out1 = target
            elif out_idx == 2:
                state.out2 = target
