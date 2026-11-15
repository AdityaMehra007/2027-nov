"""Working tree and index status comparator."""

from __future__ import annotations
from dataclasses import dataclass, field
import hashlib
import os
from typing import List, Set
from pygit.index import GitIndex
from pygit.objects import Blob
from pygit.repository import GitRepository


@dataclass
class GitStatus:
    staged: List[str] = field(default_factory=list)
    unstaged_modified: List[str] = field(default_factory=list)
    untracked: List[str] = field(default_factory=list)


def get_status(repo: GitRepository) -> GitStatus:
    index = GitIndex(repo.index_path)
    index.read()
    indexed_entries = {entry.path: entry for entry in index.entries}

    worktree_files: Set[str] = set()
    for root, dirs, files in os.walk(repo.worktree):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, repo.worktree).replace("\\", "/")
            worktree_files.add(rel_path)

    untracked: List[str] = []
    staged: List[str] = []
    unstaged_modified: List[str] = []

    for rel_path in sorted(worktree_files):
        if rel_path not in indexed_entries:
            untracked.append(rel_path)

    for path, entry in sorted(indexed_entries.items()):
        staged.append(path)
        full_path = os.path.join(repo.worktree, path)
        if not os.path.exists(full_path):
            unstaged_modified.append(path)
        else:
            with open(full_path, "rb") as f:
                content = f.read()
            current_sha = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") + b"\x00" + content).hexdigest()
            if current_sha != entry.sha:
                unstaged_modified.append(path)

    return GitStatus(
        staged=staged,
        unstaged_modified=unstaged_modified,
        untracked=untracked,
    )
