"""High-level porcelain and plumbing commands for PyGit."""

from __future__ import annotations
import os
import sys
import time
from typing import Dict, List, Optional, Tuple, Union
from pygit.diff import compute_diff
from pygit.index import GitIndex, IndexEntry
from pygit.objects import Blob, Commit, Tree, hash_object, read_object
from pygit.repository import GitRepository, find_repo, init_repo
from pygit.status import GitStatus, get_status


def _require_repo(repo: Optional[GitRepository] = None) -> GitRepository:
    if repo is not None and isinstance(repo, GitRepository):
        return repo
    found = find_repo()
    if not found:
        raise RuntimeError("fatal: not a git repository (or any of the parent directories): .git")
    return found


def cmd_init(path: str = ".", default_branch: str = "main") -> GitRepository:
    """Initialize a brand-new Git repository."""
    return init_repo(path, default_branch=default_branch)


def cmd_hash_object(
    git_dir_or_path: str,
    file_path_or_write: Union[str, bool] = False,
    write: bool = False,
) -> str:
    """Compute SHA-1 hash for a file, optionally writing it to object database."""
    if isinstance(file_path_or_write, str):
        # Called as cmd_hash_object(git_dir, file_path, write=write)
        git_dir = git_dir_or_path
        target_path = file_path_or_write
        do_write = write
    else:
        # Called as cmd_hash_object(file_path, write=bool)
        target_path = git_dir_or_path
        do_write = bool(file_path_or_write)
        repo = find_repo()
        git_dir = repo.git_dir if repo else os.path.join(".", ".git")

    with open(target_path, "rb") as f:
        data = f.read()
    blob = Blob(data)
    return hash_object(git_dir, blob, write=do_write)


def cmd_cat_file(repo_or_sha: Union[GitRepository, str], sha: Optional[str] = None) -> str:
    """Pretty-print object contents by SHA-1 hash."""
    if isinstance(repo_or_sha, GitRepository):
        git_dir = repo_or_sha.git_dir
        target_sha = sha or ""
    elif isinstance(repo_or_sha, str) and sha is not None:
        # Called as cmd_cat_file(git_dir_str, sha)
        git_dir = repo_or_sha
        target_sha = sha
    else:
        repo = _require_repo()
        git_dir = repo.git_dir
        target_sha = repo_or_sha

    obj = read_object(git_dir, target_sha)
    if isinstance(obj, Blob):
        return obj.data.decode("utf-8", errors="replace")
    elif isinstance(obj, Commit):
        return obj.serialize().decode("utf-8", errors="replace")
    elif isinstance(obj, Tree):
        lines = []
        for e in obj.entries:
            lines.append(f"{e.mode} {e.name} {e.sha}")
        return "\n".join(lines)
    return ""


def cmd_add(repo_or_paths: Union[GitRepository, List[str]], paths: Optional[List[str]] = None) -> List[str]:
    """Add file contents to the index/staging area."""
    if isinstance(repo_or_paths, GitRepository):
        repo = repo_or_paths
        target_paths = paths or []
    else:
        repo = _require_repo()
        target_paths = repo_or_paths

    index = GitIndex(repo.index_path)
    index.read()

    added: List[str] = []
    files_to_add: List[str] = []

    for p in target_paths:
        full = os.path.abspath(p) if os.path.isabs(p) else os.path.join(repo.worktree, p)
        if not os.path.exists(full):
            raise FileNotFoundError(f"fatal: pathspec '{p}' did not match any files")

        if os.path.isfile(full):
            files_to_add.append(full)
        elif os.path.isdir(full):
            for root, dirs, files in os.walk(full):
                if ".git" in dirs:
                    dirs.remove(".git")
                for f in files:
                    files_to_add.append(os.path.join(root, f))

    for file_path in sorted(files_to_add):
        rel_path = os.path.relpath(file_path, repo.worktree).replace("\\", "/")
        with open(file_path, "rb") as f:
            data = f.read()

        blob = Blob(data)
        sha = hash_object(repo.git_dir, blob, write=True)

        st = os.stat(file_path)
        mode = 0o100755 if (st.st_mode & 0o111) else 0o100644
        entry = IndexEntry(
            ctime_s=int(st.st_ctime),
            ctime_ns=int((st.st_ctime % 1) * 1e9),
            mtime_s=int(st.st_mtime),
            mtime_ns=int((st.st_mtime % 1) * 1e9),
            dev=st.st_dev,
            ino=st.st_ino,
            mode=mode,
            uid=st.st_uid,
            gid=st.st_gid,
            file_size=st.st_size,
            sha=sha,
            path=rel_path,
        )
        index.add_entry(entry)
        added.append(rel_path)

    index.write()
    return added


def cmd_write_tree(repo: Optional[GitRepository] = None) -> str:
    """Create a tree object from the current index."""
    r = _require_repo(repo)
    index = GitIndex(r.index_path)
    index.read()
    return index.write_tree(r.git_dir)


def cmd_commit(
    repo_or_msg: Union[GitRepository, str],
    message: Optional[str] = None,
    author: Optional[str] = None,
) -> str:
    """Record changes to the repository."""
    if isinstance(repo_or_msg, GitRepository):
        repo = repo_or_msg
        msg = message or ""
    else:
        repo = _require_repo()
        msg = repo_or_msg

    if not msg.strip():
        raise ValueError("Commit message cannot be empty")

    index = GitIndex(repo.index_path)
    index.read()
    if not index.entries:
        raise ValueError("nothing to commit (index is empty)")

    tree_sha = index.write_tree(repo.git_dir)

    parent = repo.get_head_commit()
    parent_shas = [parent] if parent else []

    author_name = author or "PyGit Committer <pygit@omniverse.local>"
    now_ts = int(time.time())
    author_str = f"{author_name} {now_ts} +0000"

    commit = Commit(
        tree_sha=tree_sha,
        parent_shas=parent_shas,
        author=author_str,
        committer=author_str,
        message=msg.strip(),
    )
    commit_sha = hash_object(repo.git_dir, commit, write=True)

    head_ref = repo.get_head_ref()
    if head_ref.startswith("ref: "):
        branch_ref = head_ref[5:].strip()
        repo.update_ref(branch_ref, commit_sha)
    else:
        repo.set_head_ref(commit_sha)

    return commit_sha


def cmd_status(repo: Optional[GitRepository] = None) -> GitStatus:
    """Show the working tree status."""
    r = _require_repo(repo)
    return get_status(r)


class LogEntry(dict):
    """Commit log entry supporting dict keys, tuple indexing, and (sha, message) unpacking."""

    def __getitem__(self, key):
        if isinstance(key, int):
            if key == 0:
                return self.get("sha")
            elif key == 1:
                return self.get("message")
            raise IndexError("LogEntry index out of range (0=sha, 1=message)")
        return super().__getitem__(key)

    def __iter__(self):
        yield self.get("sha")
        yield self.get("message")


def cmd_log(
    repo_or_oneline: Union[GitRepository, bool] = False,
    oneline: bool = False,
    max_count: int = 50,
) -> List[Dict[str, Union[str, List[str]]]]:
    """Show commit logs."""
    if isinstance(repo_or_oneline, GitRepository):
        repo = repo_or_oneline
        do_oneline = oneline
    else:
        repo = _require_repo()
        do_oneline = bool(repo_or_oneline)

    commits: List[Dict[str, Union[str, List[str]]]] = []
    curr_sha = repo.get_head_commit()

    visited = set()
    while curr_sha and curr_sha not in visited and len(commits) < max_count:
        visited.add(curr_sha)
        try:
            obj = read_object(repo.git_dir, curr_sha)
            if not isinstance(obj, Commit):
                break

            commits.append(LogEntry({
                "sha": curr_sha,
                "tree": obj.tree_sha,
                "parents": obj.parent_shas,
                "author": obj.author,
                "committer": obj.committer,
                "message": obj.message.strip(),
            }))
            curr_sha = obj.parent_shas[0] if obj.parent_shas else None
        except Exception:
            break

    return commits


class BranchResult(tuple):
    """Branch query result (branches_list, current_branch) supporting direct membership testing."""

    def __new__(cls, branches: List[str], current: Optional[str] = None):
        return super().__new__(cls, (branches, current))

    def __contains__(self, item: object) -> bool:
        branches, current = self
        return item in branches or item == current


def cmd_branch(
    repo_or_name: Union[GitRepository, Optional[str]] = None,
    name: Optional[str] = None,
) -> Tuple[List[str], Optional[str]]:
    """List or create branches. Returns (branch_list, current_branch)."""
    if isinstance(repo_or_name, GitRepository):
        repo = repo_or_name
        target_name = name
    else:
        repo = _require_repo()
        target_name = repo_or_name

    if target_name:
        head_commit = repo.get_head_commit()
        if not head_commit:
            raise ValueError("Cannot create branch on empty repository without commits")
        repo.create_branch(target_name, head_commit)

    branches = repo.list_branches()
    curr = repo.current_branch()
    return BranchResult(branches, curr)


def _extract_tree_files(git_dir: str, tree_sha: str, prefix: str = "") -> Dict[str, Tuple[str, str]]:
    """Recursively returns {rel_path: (mode, sha)} for all files in a tree."""
    result: Dict[str, Tuple[str, str]] = {}
    try:
        obj = read_object(git_dir, tree_sha)
        if not isinstance(obj, Tree):
            return result

        for entry in obj.entries:
            path = f"{prefix}{entry.name}"
            if entry.mode == "040000" or entry.mode.startswith("04") or entry.mode == "40000":
                sub = _extract_tree_files(git_dir, entry.sha, prefix=f"{path}/")
                result.update(sub)
            else:
                result[path] = (entry.mode, entry.sha)
    except Exception:
        pass
    return result


def cmd_checkout(repo_or_target: Union[GitRepository, str], target: Optional[str] = None) -> None:
    """Switch branches or restore working tree files."""
    if isinstance(repo_or_target, GitRepository):
        repo = repo_or_target
        dest = target or ""
    else:
        repo = _require_repo()
        dest = repo_or_target

    branch_ref_path = f"refs/heads/{dest}"
    target_commit_sha: Optional[str] = None
    is_branch = False

    ref_val = repo.get_ref(branch_ref_path)
    if ref_val:
        target_commit_sha = ref_val
        is_branch = True
    else:
        try:
            obj = read_object(repo.git_dir, dest)
            if isinstance(obj, Commit):
                target_commit_sha = dest
        except Exception:
            raise ValueError(f"Pathspec or branch '{dest}' did not match any file(s) known to git")

    if not target_commit_sha:
        raise ValueError(f"Invalid checkout target: {dest}")

    commit_obj = read_object(repo.git_dir, target_commit_sha)
    if not isinstance(commit_obj, Commit):
        raise ValueError(f"Target is not a commit: {target_commit_sha}")

    tree_files = _extract_tree_files(repo.git_dir, commit_obj.tree_sha)

    # Clean working tree files tracked by current index
    current_index = GitIndex(repo.index_path)
    current_index.read()
    for entry in current_index.entries:
        if entry.path not in tree_files:
            full = os.path.join(repo.worktree, entry.path)
            if os.path.exists(full):
                try:
                    os.remove(full)
                except OSError:
                    pass

    # Write target files to working tree and rebuild index
    new_index = GitIndex(repo.index_path)
    for path, (mode, sha) in sorted(tree_files.items()):
        blob = read_object(repo.git_dir, sha)
        if isinstance(blob, Blob):
            full_path = os.path.join(repo.worktree, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(blob.data)

            st = os.stat(full_path)
            entry = IndexEntry(
                ctime_s=int(st.st_ctime),
                ctime_ns=int((st.st_ctime % 1) * 1e9),
                mtime_s=int(st.st_mtime),
                mtime_ns=int((st.st_mtime % 1) * 1e9),
                dev=st.st_dev,
                ino=st.st_ino,
                mode=0o100644,
                uid=st.st_uid,
                gid=st.st_gid,
                file_size=st.st_size,
                sha=sha,
                path=path,
            )
            new_index.add_entry(entry)

    new_index.write()

    if is_branch:
        repo.set_head_ref(f"ref: {branch_ref_path}")
    else:
        repo.set_head_ref(target_commit_sha)


def cmd_diff(path: Optional[str] = None, repo: Optional[GitRepository] = None) -> str:
    """Generate unified diff for unstaged modified files in working tree."""
    r = _require_repo(repo)
    if path:
        return compute_diff(r, path)

    status = get_status(r)
    diffs: List[str] = []
    for p in status.unstaged_modified:
        d = compute_diff(r, p)
        if d:
            diffs.append(d)
    return "".join(diffs)


def cmd_diff_all(repo: Optional[GitRepository] = None) -> str:
    """Alias for cmd_diff()."""
    return cmd_diff(repo=repo)
