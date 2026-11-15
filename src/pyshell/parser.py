"""Shell AST parser splitting pipelines and redirection."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SimpleCommand:
    args: List[str] = field(default_factory=list)
    stdin_file: Optional[str] = None
    stdout_file: Optional[str] = None
    stdout_append: bool = False
    stderr_file: Optional[str] = None
    stderr_append: bool = False
    stderr_to_stdout: bool = False


@dataclass
class CommandLine:
    commands: List[SimpleCommand] = field(default_factory=list)
    background: bool = False


class ShellParser:
    def parse(self, line: str) -> CommandLine:
        from pyshell.lexer import ShellLexer
        lexer = ShellLexer()
        tokens = lexer.tokenize(line)
        if not tokens:
            return CommandLine()

        background = False
        if tokens and tokens[-1] == "&":
            background = True
            tokens.pop()

        cmd_line = CommandLine(background=background)
        curr_cmd = SimpleCommand()

        idx = 0
        while idx < len(tokens):
            tok = tokens[idx]

            if tok == "|":
                if curr_cmd.args:
                    cmd_line.commands.append(curr_cmd)
                    curr_cmd = SimpleCommand()
                idx += 1
            elif tok == ">":
                idx += 1
                if idx < len(tokens):
                    curr_cmd.stdout_file = tokens[idx]
                    curr_cmd.stdout_append = False
                    idx += 1
            elif tok == ">>":
                idx += 1
                if idx < len(tokens):
                    curr_cmd.stdout_file = tokens[idx]
                    curr_cmd.stdout_append = True
                    idx += 1
            elif tok == "<":
                idx += 1
                if idx < len(tokens):
                    curr_cmd.stdin_file = tokens[idx]
                    idx += 1
            elif tok == "2>":
                idx += 1
                if idx < len(tokens):
                    curr_cmd.stderr_file = tokens[idx]
                    curr_cmd.stderr_append = False
                    idx += 1
            elif tok == "2>&1":
                curr_cmd.stderr_to_stdout = True
                idx += 1
            else:
                curr_cmd.args.append(tok)
                idx += 1

        if curr_cmd.args or curr_cmd.stdout_file or curr_cmd.stdin_file:
            cmd_line.commands.append(curr_cmd)

        return cmd_line
