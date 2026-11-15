from typing import List

def insert_explicit_concat(regex: str) -> str:
    """Inserts explicit concatenation operator '.' where appropriate."""
    if not regex:
        return ""

    result = []
    unary_ops = {'*', '+', '?'}

    for i in range(len(regex)):
        c1 = regex[i]
        result.append(c1)

        if i + 1 < len(regex):
            c2 = regex[i + 1]

            # Conditions where concatenation exists between c1 and c2
            c1_is_end = (c1 not in {'|', '('})
            c2_is_start = (c2 not in {'|', ')', '*', '+', '?'})

            if c1_is_end and c2_is_start:
                result.append('.')

    return "".join(result)

def to_postfix(regex: str) -> str:
    """Converts infix regex to postfix notation using Shunting-yard algorithm."""
    expanded = insert_explicit_concat(regex)
    output: List[str] = []
    operators: List[str] = []

    precedence = {
        '*': 3, '+': 3, '?': 3,
        '.': 2,
        '|': 1
    }

    for c in expanded:
        if c in precedence:
            # Unary operators can be emitted directly or stacked
            if c in {'*', '+', '?'}:
                output.append(c)
            else:
                while (operators and operators[-1] != '(' and
                       precedence.get(operators[-1], 0) >= precedence[c]):
                    output.append(operators.pop())
                operators.append(c)
        elif c == '(':
            operators.append(c)
        elif c == ')':
            while operators and operators[-1] != '(':
                output.append(operators.pop())
            if operators and operators[-1] == '(':
                operators.pop()
        else:
            # Literal character
            output.append(c)

    while operators:
        output.append(operators.pop())

    return "".join(output)
