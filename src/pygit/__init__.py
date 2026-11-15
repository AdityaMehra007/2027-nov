"""PyGit - Canonical Git implementation from scratch in Python."""

from pygit.diff import compute_diff
from pygit.index import GitIndex, IndexEntry
from pygit.objects import Blob, Commit, GitObject, Tree, TreeEntry, hash_object, read_object
from pygit.repository import GitRepository, find_repo, init_repo
from pygit.status import GitStatus, get_status

__version__ = "0.1.0"
__all__ = [
    "GitRepository",
    "find_repo",
    "init_repo",
    "Blob",
    "Tree",
    "TreeEntry",
    "Commit",
    "GitObject",
    "hash_object",
    "read_object",
    "GitIndex",
    "IndexEntry",
    "GitStatus",
    "get_status",
    "compute_diff",
]
