"""High-level porcelain and plumbing command implementations for PyGit."""

from __future__ import annotations
import os
import time
from typing import Dict, List, Optional, Tuple, Union
from pygit.diff import compute_diff
from pygit.index import GitIndex, IndexEntry
from pygit.objects import Blob, Commit, GitObject, Tree, TreeEntry, hash_object, read_object
from pygit.repository import GitRepository, find_repo, init_repo
from pygit.status import GitStatus, get_status


def cmd_init(path: str = ".", default_branch: str = "main") -> GitRepository:
    """Initialize a brand-new Git repository."""
    return init_repo(path=path, default_branch=default_branch)


def cmd_hash_object(git_dir: str, file_path: str, write: bool = False) -> str:
    """Compute SHA-1 hash for a file, optionally writing it to object database."""
    with open(file_path, "rb") as f:
        data = f.read()
    blob = Blob(data=data)
    return hash_object(git_dir, blob, write=write)


def cmd_cat_file(git_dir: str, sha: str) -> str:
    """Pretty-print object contents by SHA-1 hash."""
    obj = read_object(git_dir, sha)
    if isinstance(obj, Blob):
        return obj.data.decode("utf-8", errors="replace")
    elif isinstance(obj, Tree):
        lines = []
        for e in obj.entries:
            lines.append(f"{e.mode} {e.name} {e.sha}")
        return "\n".join(lines)
    elif isinstance(obj, Commit):
        return obj.serialize().decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unknown object type: {type(obj)}")


def cmd_add(repo: GitRepository, paths: List[str]) -> List[str]:
    """Add file contents to the index/staging area."""
    index = GitIndex(repo.index_path)
    index.read()

    added: List[str] = []
    files_to_add: List[str] = []

    for p in paths:
        full = os.path.abspath(p) if os.path.isabs(p) else os.path.join(repo.worktree, p)
        if not os.path.exists(full):
            raise FileNotFoundError(f"Path does not exist: {p}")

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
        st = os.stat(file_path)

        with open(file_path, "rb") as f:
            content = f.read()

        blob = Blob(data=content)
        sha = hash_object(repo.git_dir, blob, write=True)

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
            path=rel_path,
        )
        index.add_entry(entry)
        added.append(rel_path)

    index.write()
    return added


def cmd_write_tree(repo: GitRepository) -> str:
    """Create a tree object from the current index."""
    index = GitIndex(repo.index_path)
    index.read()
    return index.write_tree(repo.git_dir)


def cmd_commit(
    repo: GitRepository,
    message: str,
    author: Optional[str] = None,
) -> str:
    """Record changes to the repository."""
    if not message.strip():
        raise ValueError("Commit message cannot be empty")

    index = GitIndex(repo.index_path)
    index.read()
    if not index.entries:
        raise ValueError("Nothing to commit (index is empty)")

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
        message=message.strip(),
    )
    commit_sha = hash_object(repo.git_dir, commit, write=True)

    # Update branch ref or detached HEAD
    head_ref = repo.get_head_ref()
    if head_ref.startswith("ref: "):
        branch_ref = head_ref[5:].strip()
        repo.update_ref(branch_ref, commit_sha)
    else:
        repo.set_head_ref(commit_sha)

    return commit_sha


def cmd_status(repo: GitRepository) -> GitStatus:
    """Show the working tree status."""
    return get_status(repo)


def cmd_log(repo: GitRepository, max_count: Optional[int] = None) -> List[Dict[str, Union[str, List[str]]]]:
    """Show commit logs."""
    commits: List[Dict[str, Union[str, List[str]]]] = []
    curr_sha = repo.get_head_commit()

    while curr_sha:
        if max_count and len(commits) >= max_count:
            break
        try:
            obj = read_object(repo.git_dir, curr_sha)
            if not isinstance(obj, Commit):
                break

            commits.append({
                "sha": curr_sha,
                "tree": obj.tree_sha,
                "parents": obj.parent_shas,
                "author": obj.author,
                "committer": obj.committer,
                "message": obj.message.strip(),
            })
            curr_sha = obj.parent_shas[0] if obj.parent_shas else None
        except Exception:
            break

    return commits


def cmd_branch(repo: GitRepository, name: Optional[str] = None) -> Tuple[List[str], Optional[str]]:
    """List or create branches. Returns (branch_list, current_branch)."""
    if name:
        head_commit = repo.get_head_commit()
        if not head_commit:
            raise ValueError("Cannot create branch on empty repository without commits")
        repo.create_branch(name, head_commit)

    branches = repo.list_branches()
    curr = repo.current_branch()
    return branches, curr


def _extract_tree_files(git_dir: str, tree_sha: str, prefix: str = "") -> Dict[str, Tuple[str, str]]:
    """Recursively returns {rel_path: (mode, sha)} for all files in a tree."""
    result: Dict[str, Tuple[str, str]] = {}
    obj = read_object(git_dir, tree_sha)
    if not isinstance(obj, Tree):
        return result

    for entry in obj.entries:
        path = f"{prefix}{entry.name}"
        if entry.mode == "040000" or entry.mode.startswith("04") or entry.mode == "40000":
            # Subtree
            sub = _extract_tree_files(git_dir, entry.sha, prefix=f"{path}/")
            result.update(sub)
        else:
            result[path] = (entry.mode, entry.sha)

    return result


def cmd_checkout(repo: GitRepository, target: str) -> None:
    """Switch branches or restore working tree files."""
    branch_ref_path = f"refs/heads/{target}"
    target_commit_sha: Optional[str] = None
    is_branch = False

    ref_val = repo.get_ref(branch_ref_path)
    if ref_val:
        target_commit_sha = ref_val
        is_branch = True
    else:
        # Check if target is a raw commit SHA
        try:
            obj = read_object(repo.git_dir, target)
            if isinstance(obj, Commit):
                target_commit_sha = target
        except Exception:
            raise ValueError(f"Pathspec or branch '{target}' did not match any file(s) known to git")

    if not target_commit_sha:
        raise ValueError(f"Invalid checkout target: {target}")

    commit_obj = read_object(repo.git_dir, target_commit_sha)
    if not isinstance(commit_obj, Commit):
        raise ValueError(f"Target is not a commit: {target_commit_sha}")

    # Extract all files in target commit tree
    tree_files = _extract_tree_files(repo.git_dir, commit_obj.tree_sha)

    # Clean working tree files tracked by current index
    current_index = GitIndex(repo.index_path)
    current_index.read()
    for entry in current_index.entries:
        if entry.path not in tree_files:
            full = os.path.join(repo.worktree, entry.path)
            if os.path.exists(full):
                os.remove(full)

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

    # Update HEAD
    if is_branch:
        repo.set_head_ref(f"ref: {branch_ref_path}")
    else:
        repo.set_head_ref(target_commit_sha)


def cmd_diff_all(repo: GitRepository) -> str:
    """Generate unified diff for all unstaged modified files in working tree."""
    status = get_status(repo)
    diffs: List[str] = []
    for path in status.unstaged_modified:
        d = compute_diff(repo, path)
        if d:
            diffs.append(d)
    return "".join(diffs)
