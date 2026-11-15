"""Shell command execution engine with builtins, pipes, and redirects."""

from __future__ import annotations
import io
import os
import shutil
import subprocess
import sys
from typing import Dict, List, Optional
from pyshell.parser import CommandLine, ShellParser, SimpleCommand


class ShellExecutor:
    def __init__(self) -> None:
        self.env: Dict[str, str] = dict(os.environ)
        self.history: List[str] = []
        self.parser = ShellParser()
        self.builtins = {
            "cd": self._builtin_cd,
            "pwd": self._builtin_pwd,
            "exit": self._builtin_exit,
            "echo": self._builtin_echo,
            "export": self._builtin_export,
            "history": self._builtin_history,
            "type": self._builtin_type,
            "which": self._builtin_which,
        }

    def run_line(self, line: str) -> str:
        line_clean = line.strip()
        if not line_clean:
            return ""

        self.history.append(line_clean)
        cmd_line = self.parser.parse(line_clean)
        if not cmd_line.commands:
            return ""

        return self.execute_pipeline(cmd_line)

    def execute_pipeline(self, cmd_line: CommandLine) -> str:
        # If single builtin without external pipes, execute directly in-process
        if len(cmd_line.commands) == 1 and cmd_line.commands[0].args:
            first_cmd = cmd_line.commands[0]
            cmd_name = first_cmd.args[0]
            if cmd_name in self.builtins:
                out = self.builtins[cmd_name](first_cmd.args[1:])
                # Handle redirection if present
                if first_cmd.stdout_file:
                    mode = "a" if first_cmd.stdout_append else "w"
                    with open(first_cmd.stdout_file, mode, encoding="utf-8") as f:
                        f.write(out + "\n" if not out.endswith("\n") else out)
                    return ""
                return out

        # Pipeline of external commands or piped builtins
        stdin_stream = None
        current_input = None

        output_acc = []

        for i, cmd in enumerate(cmd_line.commands):
            if not cmd.args:
                continue

            cmd_name = cmd.args[0]
            # Variable expansion
            expanded_args = [self._expand_vars(a) for a in cmd.args]

            # In-process builtin execution within pipeline
            if cmd_name in self.builtins:
                builtin_out = self.builtins[cmd_name](expanded_args[1:])
                current_input = builtin_out.encode("utf-8")
                if i == len(cmd_line.commands) - 1:
                    output_acc.append(builtin_out)
                continue

            # External process
            stdout_target = subprocess.PIPE
            if i == len(cmd_line.commands) - 1 and cmd.stdout_file:
                mode = "ab" if cmd.stdout_append else "wb"
                stdout_target = open(cmd.stdout_file, mode)

            stdin_target = subprocess.PIPE if current_input else None
            if cmd.stdin_file and os.path.exists(cmd.stdin_file):
                stdin_target = open(cmd.stdin_file, "rb")

            try:
                proc = subprocess.Popen(
                    expanded_args,
                    stdin=stdin_target,
                    stdout=stdout_target,
                    stderr=subprocess.PIPE,
                    env=self.env,
                    shell=False,
                )

                stdout_data, stderr_data = proc.communicate(input=current_input if stdin_target == subprocess.PIPE else None)
                if stdout_target == subprocess.PIPE and stdout_data:
                    current_input = stdout_data
                    if i == len(cmd_line.commands) - 1:
                        output_acc.append(stdout_data.decode("utf-8", errors="replace"))

            except Exception as e:
                err_msg = f"pyshell: {cmd_name}: {e}\n"
                output_acc.append(err_msg)
            finally:
                if isinstance(stdout_target, io.IOBase) and not stdout_target.closed:
                    stdout_target.close()
                if isinstance(stdin_target, io.IOBase) and not stdin_target.closed:
                    stdin_target.close()

        return "".join(output_acc)

    def _expand_vars(self, s: str) -> str:
        for k, v in self.env.items():
            s = s.replace(f"${k}", v)
        return s

    # -------------------------------------------------------------------------
    # Builtin Implementations
    # -------------------------------------------------------------------------

    def _builtin_cd(self, args: List[str]) -> str:
        target = args[0] if args else self.env.get("HOME", ".")
        try:
            os.chdir(target)
            return ""
        except Exception as e:
            return f"cd: {e}\n"

    def _builtin_pwd(self, args: List[str]) -> str:
        return os.getcwd() + "\n"

    def _builtin_exit(self, args: List[str]) -> str:
        code = int(args[0]) if args and args[0].isdigit() else 0
        sys.exit(code)

    def _builtin_echo(self, args: List[str]) -> str:
        expanded = [self._expand_vars(a) for a in args]
        return " ".join(expanded) + "\n"

    def _builtin_export(self, args: List[str]) -> str:
        for arg in args:
            if "=" in arg:
                k, v = arg.split("=", 1)
                self.env[k] = v
                os.environ[k] = v
        return ""

    def _builtin_history(self, args: List[str]) -> str:
        lines = []
        for i, cmd in enumerate(self.history, 1):
            lines.append(f"{i:4d}  {cmd}")
        return "\n".join(lines) + "\n"

    def _builtin_type(self, args: List[str]) -> str:
        if not args:
            return ""
        name = args[0]
        if name in self.builtins:
            return f"{name} is a shell builtin\n"
        path = shutil.which(name)
        if path:
            return f"{name} is {path}\n"
        return f"{name}: not found\n"

    def _builtin_which(self, args: List[str]) -> str:
        if not args:
            return ""
        path = shutil.which(args[0])
        return f"{path}\n" if path else f"{args[0]} not found\n"
