# PyGit: Git from Scratch Design Specification

**Date:** 2026-11-14  
**System:** Distributed Version Control System (PyGit)  
**Language & Runtime:** Python 3.13+ (Standard Library only, zero external dependencies)  
**Status:** Approved for Implementation

---

## 1. Executive Summary & Goals

PyGit is a zero-dependency, canonical implementation of Git built from scratch in Python. It directly produces and consumes real Git object stores and binary index files, ensuring 100% interoperability with official `git`.

### Key Goals
1. **Zero External Dependencies:** Built with Python standard library (`hashlib`, `zlib`, `struct`, `os`, `sys`, `time`, `difflib`, `argparse`, `unittest`).
2. **Canonical Git Object Storage:** Implements `blob`, `tree`, and `commit` objects with SHA-1 content addressing and `zlib` compression.
3. **DIRC v2 Binary Index:** Full reading and writing of `.git/index` binary staging cache with 8-byte alignment and SHA-1 checksum.
4. **Porcelain & Plumbing Commands:** `init`, `hash-object`, `cat-file`, `write-tree`, `add`, `commit`, `status`, `log`, `branch`, `checkout`, `diff`.
5. **Real Git Interoperability:** Official `git` CLI can inspect repos initialized and committed by PyGit, and PyGit can inspect repos initialized by `git`.

---

## 2. Architecture & File Structure

```
src/pygit/
├── __init__.py
├── objects.py      # GitObject, Blob, Tree, Commit, zlib read/write & SHA-1
├── index.py        # DIRC v2 binary parser, serializer & index entry management
├── repository.py   # .git repo finder, refs manager (HEAD, refs/heads/*)
├── status.py       # Working tree vs index vs HEAD status comparison
├── diff.py         # Unified diff generator for modified files
├── commands.py     # Porcelain & plumbing command dispatch logic
└── cli.py          # Entrypoint CLI for python -m pygit
```

---

## 3. Object Model

- Format: `<type> <size>\x00<data>`
- SHA-1: 40-character hex string of `sha1(f"{type} {len(data)}\x00{data}")`
- Path on disk: `.git/objects/<sha1[:2]>/<sha1[2:]>` compressed with `zlib.compress()`.

### Object Types
- **Blob:** Raw file content bytes.
- **Tree:** Binary list of directory entries formatted as:
  `{mode_octal_str} {name}\x00{20_byte_binary_sha}` (e.g. `100644 file.txt\x00...`)
- **Commit:** Text header containing `tree <sha1>`, optional `parent <sha1>`, `author`, `committer`, and message.

---

## 4. DIRC v2 Binary Index (`.git/index`)

- Header (12 bytes):
  - Signature: `DIRC` (4 bytes)
  - Version: `2` (4 bytes big-endian)
  - Number of entries: `N` (4 bytes big-endian)
- Entry format (multiples of 8 bytes):
  - `ctime` (8 bytes)
  - `mtime` (8 bytes)
  - `dev` (4 bytes), `ino` (4 bytes), `mode` (4 bytes)
  - `uid` (4 bytes), `gid` (4 bytes), `file_size` (4 bytes)
  - `sha1` (20 bytes)
  - `flags` (2 bytes)
  - `name` (null-terminated string)
  - `padding` (1-8 null bytes to reach 8-byte alignment)
- Checksum: Trailing 20-byte SHA-1 digest over the entire preceding content.

---

## 5. Command Specifications

- `init [dir]`: Writes `.git/`, `.git/objects/`, `.git/refs/heads/`, and `HEAD` (`ref: refs/heads/main\n`).
- `hash-object [-w] file`: Hashes file and optionally writes to `.git/objects/`.
- `cat-file -p sha`: Pretty prints object contents.
- `add path [paths...]`: Hashes file to blob, creates/updates entry in `.git/index`.
- `write-tree`: Recursively serializes index entries to `Tree` objects, returns root tree SHA-1.
- `commit -m message`: Writes root tree from index, creates commit object with current HEAD as parent, updates current branch ref.
- `status`: Reports staged changes, unstaged changes, and untracked files.
- `log [--oneline]`: Traverses parent commits from HEAD backwards, printing history.
- `branch [name]`: Lists branches or creates new branch ref.
- `checkout target`: Switches branch/commit, updates working tree files.
- `diff`: Compares working tree against index.

---

## 6. Testing & Verification Plan

1. `tests/test_pygit_objects.py`: Serialization, SHA-1 computation, zlib reading/writing.
2. `tests/test_pygit_index.py`: DIRC v2 binary parsing, writing, checksum validation, tree generation.
3. `tests/test_pygit_commands.py`: End-to-end testing of `init`, `add`, `commit`, `status`, `log`, `branch`, `checkout`, `diff`.
4. Interoperability verification: Verifying against real `git` CLI where available.
