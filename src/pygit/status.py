"""Status engine comparing working directory, index, and HEAD commit."""

from __future__ import annotations
from dataclasses import dataclass, field
import hashlib
import os
from typing import Dict, List, Set
from pygit.index import GitIndex
from pygit.objects import Blob, Commit, Tree, read_object
from pygit.repository import GitRepository


@dataclass
class RepoStatus:
    staged: List[str] = field(default_factory=list)
    unstaged_modified: List[str] = field(default_factory=list)
    unstaged_deleted: List[str] = field(default_factory=list)
    untracked: List[str] = field(default_factory=list)


GitStatus = RepoStatus


GitStatus = RepoStatus

# Alias for compatibility
GitStatus = RepoStatus


def _get_tree_files(git_dir: str, tree_sha: str, prefix: str = "") -> Dict[str, str]:
    """Recursively traverses a Git tree and returns a mapping of relative path -> blob sha."""
    tree_map: Dict[str, str] = {}
    try:
        obj = read_object(git_dir, tree_sha)
        if not isinstance(obj, Tree):
            return tree_map
        for entry in obj.entries:
            path = os.path.join(prefix, entry.name).replace("\\", "/")
            if entry.mode == "040000" or entry.mode.startswith("04"):
                sub_map = _get_tree_files(git_dir, entry.sha, prefix=path)
                tree_map.update(sub_map)
            else:
                tree_map[path] = entry.sha
    except Exception:
        pass
    return tree_map


def get_status(repo: GitRepository) -> RepoStatus:
    status = RepoStatus()

    # 1. Read Index
    index = GitIndex(repo.index_path)
    index.read()
    index_map = {e.path: e for e in index.entries}

    # 2. Read HEAD commit files
    head_files: Dict[str, str] = {}
    head_sha = repo.get_head_commit()
    if head_sha:
        try:
            head_commit = read_object(repo.git_dir, head_sha)
            if isinstance(head_commit, Commit):
                head_files = _get_tree_files(repo.git_dir, head_commit.tree_sha)
        except Exception:
            pass

    # 3. Compare Index vs HEAD (Staged changes)
    for path, entry in index_map.items():
        if path not in head_files:
            status.staged.append(path)
        elif head_files[path] != entry.sha:
            status.staged.append(path)

    # 4. Scan Working Tree
    worktree_files: Set[str] = set()
    for root, dirs, files in os.walk(repo.worktree):
        # Ignore .git and common ignores
        if ".git" in dirs:
            dirs.remove(".git")
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")

        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, repo.worktree).replace("\\", "/")
            worktree_files.add(rel)

    # 5. Check Working Tree vs Index (Unstaged & Untracked)
    for path in sorted(worktree_files):
        if path not in index_map:
            status.untracked.append(path)
        else:
            entry = index_map[path]
            full_path = os.path.join(repo.worktree, path)
            try:
                st = os.stat(full_path)
                # Quick check: file size or mtime change
                if st.st_size != entry.file_size or int(st.st_mtime) != entry.mtime_s:
                    # Content check
                    with open(full_path, "rb") as f:
                        data = f.read()
                    blob = Blob(data)
                    if blob.sha1() != entry.sha:
                        status.unstaged_modified.append(path)
            except OSError:
                pass

    for path in sorted(index_map.keys()):
        if path not in worktree_files:
            status.unstaged_deleted.append(path)

    return status
