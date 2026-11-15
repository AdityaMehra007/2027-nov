"""Interactive REPL and CLI runner for PyShell."""

from __future__ import annotations
import argparse
import os
import sys
from pyshell.executor import ShellExecutor


def run_repl() -> None:
    executor = ShellExecutor()
    print("PyShell v0.1.0 - Interactive POSIX-style shell from scratch")
    print("Type 'exit' to quit, 'help' for built-ins.\n")

    while True:
        try:
            cwd = os.getcwd()
            home = os.path.expanduser("~")
            display_dir = cwd.replace(home, "~")
            prompt = f"\033[36mpyshell\033[0m:\033[33m{display_dir}\033[0m$ "
            line = input(prompt)
            if not line.strip():
                continue

            output = executor.run_line(line)
            if output:
                print(output, end="" if output.endswith("\n") else "\n")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting PyShell.")
            break
        except SystemExit:
            break
        except Exception as e:
            print(f"pyshell: {e}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(prog="pyshell", description="PyShell - Unix Shell from Scratch")
    parser.add_argument("-c", "--command", help="Execute command string and exit")
    args = parser.parse_args()

    executor = ShellExecutor()
    if args.command:
        out = executor.run_line(args.command)
        if out:
            print(out, end="" if out.endswith("\n") else "\n")
    else:
        run_repl()


if __name__ == "__main__":
    main()
