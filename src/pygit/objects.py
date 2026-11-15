"""Canonical Git object model: Blob, Tree, Commit, and Tag with zlib compression."""

from __future__ import annotations
from dataclasses import dataclass, field
import hashlib
import os
from typing import ClassVar, List, Optional
import zlib


class GitObject:
    obj_type: ClassVar[str] = "unknown"

    def serialize(self) -> bytes:
        raise NotImplementedError

    def full_payload(self) -> bytes:
        data = self.serialize()
        header = f"{self.obj_type} {len(data)}\x00".encode("ascii")
        return header + data

    def sha1(self) -> str:
        return hashlib.sha1(self.full_payload()).hexdigest()


@dataclass
class Blob(GitObject):
    data: bytes
    obj_type: ClassVar[str] = "blob"

    def serialize(self) -> bytes:
        return self.data


@dataclass
class TreeEntry:
    mode: str
    name: str
    sha: str

    def serialize(self) -> bytes:
        # Format: "<mode> <name>\x00<20-byte binary sha>"
        # Normalize mode (e.g. "100644" or "40000" -> "040000")
        mode_str = self.mode.lstrip("0") if self.mode.startswith("0") else self.mode
        return f"{mode_str} {self.name}\x00".encode("utf-8") + bytes.fromhex(self.sha)


@dataclass
class Tree(GitObject):
    entries: List[TreeEntry] = field(default_factory=list)
    obj_type: ClassVar[str] = "tree"

    def serialize(self) -> bytes:
        # Git sorts tree entries with a special rule: directories sort as if ending with '/'
        def sort_key(e: TreeEntry):
            return e.name + "/" if e.mode.startswith("04") or e.mode == "40000" else e.name

        sorted_entries = sorted(self.entries, key=sort_key)
        out = bytearray()
        for e in sorted_entries:
            out.extend(e.serialize())
        return bytes(out)

    @classmethod
    def parse(cls, data: bytes) -> Tree:
        entries: List[TreeEntry] = []
        pos = 0
        length = len(data)

        while pos < length:
            null_idx = data.find(b"\x00", pos)
            if null_idx == -1:
                break
            header = data[pos:null_idx].decode("utf-8")
            mode, name = header.split(" ", 1)
            # Normalize directory mode
            if mode == "40000":
                mode = "040000"

            pos = null_idx + 1
            raw_sha = data[pos : pos + 20]
            sha = raw_sha.hex()
            pos += 20
            entries.append(TreeEntry(mode=mode, name=name, sha=sha))

        return cls(entries=entries)


@dataclass
class Commit(GitObject):
    tree_sha: str
    parent_shas: List[str]
    author: str
    committer: str
    message: str
    obj_type: ClassVar[str] = "commit"

    def serialize(self) -> bytes:
        lines: List[str] = [f"tree {self.tree_sha}"]
        for p in self.parent_shas:
            lines.append(f"parent {p}")
        lines.append(f"author {self.author}")
        lines.append(f"committer {self.committer}")
        lines.append("")
        lines.append(self.message.rstrip("\n") + "\n")
        return "\n".join(lines).encode("utf-8")

    @classmethod
    def parse(cls, data: bytes) -> Commit:
        text = data.decode("utf-8", errors="replace")
        header_part, _, message = text.partition("\n\n")

        tree_sha = ""
        parent_shas = []
        author = ""
        committer = ""

        for line in header_part.splitlines():
            if line.startswith("tree "):
                tree_sha = line[5:].strip()
            elif line.startswith("parent "):
                parent_shas.append(line[7:].strip())
            elif line.startswith("author "):
                author = line[7:].strip()
            elif line.startswith("committer "):
                committer = line[10:].strip()

        return cls(
            tree_sha=tree_sha,
            parent_shas=parent_shas,
            author=author,
            committer=committer,
            message=message,
        )


def hash_object(git_dir: str, obj: GitObject, write: bool = False) -> str:
    payload = obj.full_payload()
    sha = hashlib.sha1(payload).hexdigest()

    if write:
        obj_dir = os.path.join(git_dir, "objects", sha[:2])
        obj_path = os.path.join(obj_dir, sha[2:])
        if not os.path.exists(obj_path):
            os.makedirs(obj_dir, exist_ok=True)
            compressed = zlib.compress(payload)
            with open(obj_path, "wb") as f:
                f.write(compressed)

    return sha


def read_object(git_dir: str, sha: str) -> GitObject:
    obj_path = os.path.join(git_dir, "objects", sha[:2], sha[2:])
    if not os.path.exists(obj_path):
        raise FileNotFoundError(f"Git object not found: {sha}")

    with open(obj_path, "rb") as f:
        decompressed = zlib.decompress(f.read())

    null_idx = decompressed.find(b"\x00")
    if null_idx == -1:
        raise ValueError(f"Corrupt git object: {sha}")

    header = decompressed[:null_idx].decode("ascii")
    obj_type, _ = header.split(" ", 1)
    data = decompressed[null_idx + 1 :]

    if obj_type == "blob":
        return Blob(data=data)
    elif obj_type == "tree":
        return Tree.parse(data)
    elif obj_type == "commit":
        return Commit.parse(data)
    else:
        raise ValueError(f"Unsupported git object type: {obj_type}")
