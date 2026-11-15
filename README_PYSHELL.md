# PyShell: Interactive Unix Shell from Scratch in Python

A zero-dependency, POSIX-style interactive shell implementation built with Python 3.13 standard library.

---

## Features

- **Lexer & Quoting Engine:** Precise tokenization of single quotes (`'...'`), double quotes (`"..."`), and escape characters (`\ `).
- **Pipelines & Redirection:**
  - Pipe chaining: `cmd1 | cmd2 | cmd3`
  - Output redirection: `> file` and `>> file`
  - Input redirection: `< file`
  - Error redirection: `2> file` and `2>&1`
- **Shell Builtins:** `cd`, `pwd`, `echo`, `export`, `history`, `type`, `which`, `exit`.
- **Environment & Variable Expansion:** Dynamic expansion of `$VAR` in command parameters.
- **Interactive REPL:** Styled terminal prompt showing current working directory and history navigation.

---

## Quickstart Usage

```bash
# 1. Start interactive shell
python -m pyshell

pyshell:~$ cd my_project
pyshell:~/my_project$ echo "Hello PyShell" > note.txt
pyshell:~/my_project$ cat note.txt | tr 'a-z' 'A-Z'
HELLO PYSHELL

pyshell:~/my_project$ export APP_ENV=production
pyshell:~/my_project$ echo "Environment: $APP_ENV"
Environment: production

pyshell:~/my_project$ type echo
echo is a shell builtin

pyshell:~/my_project$ exit
```

---

## Running Tests

```bash
python -m unittest tests/test_pyshell.py
```
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.050s

OK
```
