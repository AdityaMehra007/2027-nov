# PyGit: Git from Scratch in Python

A complete, zero-dependency implementation of Git built entirely in Python 3.13 standard library. PyGit directly creates, parses, and manages real Git content-addressed object databases (`blob`, `tree`, `commit`), DIRC v2 binary staging indices, and branch references.

PyGit is 100% interoperable with official `git`: you can run `git status`, `git log`, or `git checkout` on a repo initialized by PyGit, and vice-versa!

---

## Architecture Overview

```
                           pygit CLI / API
                                  |
                                  v
+-------------------------------------------------------------------+
|                        Porcelain Commands                         |
|   init | add | commit | status | log | branch | checkout | diff   |
+---------------------------------+---------------------------------+
                                  |
            +---------------------+---------------------+
            |                                           |
            v                                           v
+-----------------------+                   +-----------------------+
|  DIRC v2 Binary Index |                   |  Object Store (.git)  |
|      (index.py)       |                   |      (objects.py)     |
|   - Stat cache        |                   |   - Blob (file bytes) |
|   - 8-byte alignment  | === write-tree => |   - Tree (dir entries)|
|   - SHA-1 checksum    |                   |   - Commit (metadata) |
+-----------------------+                   |   - zlib compression  |
                                            +-----------------------+
```

---

## Features

- **Content-Addressed Storage:** Exact `<type> <size>\x00<data>` framing, SHA-1 object ID computation, and zlib-compressed storage in `.git/objects/<2-hex>/<38-hex>`.
- **DIRC v2 Binary Index Parser & Writer:** Full support for `.git/index` binary staging cache with 8-byte entry alignment and trailing 20-byte SHA-1 integrity checksums.
- **Hierarchical Tree Serialization (`write-tree`):** Converts flat index paths into nested, sorted Git tree objects bottom-up.
- **Reference & Branch Management:** Resolves symbolic refs (`ref: refs/heads/main`) and detached HEAD pointers.
- **Working Tree Synchronization:** Clean branch checkout restoring directory trees and index metadata.
- **Unified Diff Generation:** Native line-by-line diffing between working directory and staged blobs using Python's `difflib`.

---

## Quickstart CLI Usage

```bash
# 1. Initialize a new repo
python -m pygit init my_project
cd my_project

# 2. Stage files
echo "Hello World" > hello.txt
python -m pygit add hello.txt

# 3. Check status
python -m pygit status

# 4. Commit changes
python -m pygit commit -m "feat: initial commit from PyGit"

# 5. Inspect commit log
python -m pygit log --oneline

# 6. Branch and checkout
python -m pygit branch feature
python -m pygit checkout feature
```

---

## Running Test Suite

PyGit requires zero third-party packages. Run all tests with standard `unittest`:

```bash
python -m unittest discover -s tests -p "test_pygit_*.py"
```
```
...........
----------------------------------------------------------------------
Ran 11 tests in 2.451s

OK
```
