"""Unified diff generator comparing working copy against Git index."""

from __future__ import annotations
import difflib
import os
from typing import List, Optional
from pygit.index import GitIndex
from pygit.objects import Blob, read_object
from pygit.repository import GitRepository


def compute_diff(repo: GitRepository, rel_path: str) -> str:
    """Computes a unified diff for a single file between index and working tree."""
    index = GitIndex(repo.index_path)
    index.read()
    entry = index.get_entry(rel_path)

    old_lines: List[str] = []
    if entry:
        try:
            blob = read_object(repo.git_dir, entry.sha)
            if isinstance(blob, Blob):
                old_lines = blob.data.decode("utf-8", errors="replace").splitlines(keepends=True)
        except Exception:
            old_lines = []

    full_path = os.path.join(repo.worktree, rel_path)
    new_lines: List[str] = []
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            new_lines = f.readlines()

    diff_lines = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}",
        )
    )
    return "".join(diff_lines)
