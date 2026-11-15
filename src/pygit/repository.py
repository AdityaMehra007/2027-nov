"""Git repository filesystem layout and reference management."""

from __future__ import annotations
import configparser
import os
from typing import List, Optional


class GitRepository:
    def __init__(self, worktree: str, git_dir: Optional[str] = None) -> None:
        self.worktree = os.path.abspath(worktree)
        self.git_dir = os.path.abspath(git_dir or os.path.join(self.worktree, ".git"))

    @property
    def index_path(self) -> str:
        return os.path.join(self.git_dir, "index")

    def get_head_ref(self) -> str:
        head_file = os.path.join(self.git_dir, "HEAD")
        if not os.path.exists(head_file):
            return ""
        with open(head_file, "r", encoding="utf-8") as f:
            return f.read().strip()

    def set_head_ref(self, ref_or_sha: str) -> None:
        head_file = os.path.join(self.git_dir, "HEAD")
        with open(head_file, "w", encoding="utf-8") as f:
            f.write(ref_or_sha + "\n")

    def get_ref(self, ref_name: str) -> Optional[str]:
        ref_path = os.path.join(self.git_dir, ref_name)
        if not os.path.exists(ref_path):
            return None
        with open(ref_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def update_ref(self, ref_name: str, sha: str) -> None:
        ref_path = os.path.join(self.git_dir, ref_name)
        os.makedirs(os.path.dirname(ref_path), exist_ok=True)
        with open(ref_path, "w", encoding="utf-8") as f:
            f.write(sha.strip() + "\n")

    def get_head_commit(self) -> Optional[str]:
        head_ref = self.get_head_ref()
        if not head_ref:
            return None
        if head_ref.startswith("ref: "):
            target = head_ref[5:].strip()
            return self.get_ref(target)
        # Detached HEAD pointing directly to commit SHA
        return head_ref

    def current_branch(self) -> Optional[str]:
        head_ref = self.get_head_ref()
        if head_ref.startswith("ref: refs/heads/"):
            return head_ref[16:].strip()
        return None

    def create_branch(self, name: str, sha: str) -> None:
        self.update_ref(f"refs/heads/{name}", sha)

    def list_branches(self) -> List[str]:
        heads_dir = os.path.join(self.git_dir, "refs", "heads")
        if not os.path.exists(heads_dir):
            return []
        branches: List[str] = []
        for root, _, files in os.walk(heads_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel = os.path.relpath(full_path, heads_dir).replace("\\", "/")
                branches.append(rel)
        return sorted(branches)


def init_repo(path: str = ".", default_branch: str = "main") -> GitRepository:
    worktree = os.path.abspath(path)
    git_dir = os.path.join(worktree, ".git")

    os.makedirs(os.path.join(git_dir, "objects"), exist_ok=True)
    os.makedirs(os.path.join(git_dir, "refs", "heads"), exist_ok=True)
    os.makedirs(os.path.join(git_dir, "refs", "tags"), exist_ok=True)

    # Write initial HEAD
    head_file = os.path.join(git_dir, "HEAD")
    if not os.path.exists(head_file):
        with open(head_file, "w", encoding="utf-8") as f:
            f.write(f"ref: refs/heads/{default_branch}\n")

    # Write basic config
    config_file = os.path.join(git_dir, "config")
    if not os.path.exists(config_file):
        cfg = configparser.ConfigParser()
        cfg["core"] = {
            "repositoryformatversion": "0",
            "filemode": "false",
            "bare": "false",
        }
        with open(config_file, "w", encoding="utf-8") as f:
            cfg.write(f)

    return GitRepository(worktree=worktree, git_dir=git_dir)


def find_repo(start_path: str = ".") -> Optional[GitRepository]:
    curr = os.path.abspath(start_path)
    while True:
        git_dir = os.path.join(curr, ".git")
        if os.path.isdir(git_dir):
            return GitRepository(worktree=curr, git_dir=git_dir)
        parent = os.path.dirname(curr)
        if parent == curr:
            # Reached root of drive
            break
        curr = parent
    return None
