"""DIRC v2 Binary Index parser, serializer, and tree construction for Git."""

from __future__ import annotations
from dataclasses import dataclass
import hashlib
import os
import struct
from typing import Dict, List, Optional
from pygit.objects import Tree, TreeEntry, hash_object


@dataclass
class IndexEntry:
    ctime_s: int
    ctime_ns: int
    mtime_s: int
    mtime_ns: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    file_size: int
    sha: str
    path: str
    flags: int = 0

    def serialize(self) -> bytes:
        raw_sha = bytes.fromhex(self.sha)
        encoded_path = self.path.encode("utf-8")
        # Flags: 16-bit integer, lowest 12 bits store path length (capped at 0xFFF)
        flags = self.flags if self.flags else min(len(encoded_path), 0xFFF)

        # Packed metadata: 10 ints + 20-byte SHA + 2-byte flags = 62 bytes
        fixed = struct.pack(
            ">IIIIIIIIII20sH",
            self.ctime_s & 0xFFFFFFFF,
            self.ctime_ns & 0xFFFFFFFF,
            self.mtime_s & 0xFFFFFFFF,
            self.mtime_ns & 0xFFFFFFFF,
            self.dev & 0xFFFFFFFF,
            self.ino & 0xFFFFFFFF,
            self.mode & 0xFFFFFFFF,
            self.uid & 0xFFFFFFFF,
            self.gid & 0xFFFFFFFF,
            self.file_size & 0xFFFFFFFF,
            raw_sha,
            flags,
        )

        entry_bytes = fixed + encoded_path + b"\x00"
        # Pad with null bytes to a multiple of 8 bytes
        pad_len = 8 - (len(entry_bytes) % 8)
        if pad_len == 8:
            pad_len = 0
        elif pad_len == 0:
            pad_len = 8
        # Standard Git pads 1-8 bytes to align on an 8-byte boundary relative to entry start
        rem = len(entry_bytes) % 8
        if rem != 0:
            entry_bytes += b"\x00" * (8 - rem)

        return entry_bytes

    @classmethod
    def parse(cls, data: bytes, offset: int) -> tuple[IndexEntry, int]:
        fixed = data[offset : offset + 62]
        (
            ctime_s,
            ctime_ns,
            mtime_s,
            mtime_ns,
            dev,
            ino,
            mode,
            uid,
            gid,
            file_size,
            raw_sha,
            flags,
        ) = struct.unpack(">IIIIIIIIII20sH", fixed)

        sha = raw_sha.hex()
        path_start = offset + 62
        path_end = data.find(b"\x00", path_start)
        path = data[path_start:path_end].decode("utf-8", errors="replace")

        # Advance past path, null terminator, and padding to 8-byte boundary
        entry_end = path_end + 1
        rem = (entry_end - offset) % 8
        if rem != 0:
            entry_end += 8 - rem

        entry = cls(
            ctime_s=ctime_s,
            ctime_ns=ctime_ns,
            mtime_s=mtime_s,
            mtime_ns=mtime_ns,
            dev=dev,
            ino=ino,
            mode=mode,
            uid=uid,
            gid=gid,
            file_size=file_size,
            sha=sha,
            path=path,
            flags=flags,
        )
        return entry, entry_end


class GitIndex:
    def __init__(self, index_path: str) -> None:
        self.index_path = index_path
        self.entries: List[IndexEntry] = []

    def read(self) -> None:
        if not os.path.exists(self.index_path):
            self.entries = []
            return

        with open(self.index_path, "rb") as f:
            data = f.read()

        if len(data) < 32:
            self.entries = []
            return

        # Check signature & version
        sig, version, count = struct.unpack(">4sII", data[:12])
        if sig != b"DIRC":
            raise ValueError(f"Invalid git index signature: {sig}")

        offset = 12
        entries: List[IndexEntry] = []
        for _ in range(count):
            if offset >= len(data) - 20:
                break
            entry, offset = IndexEntry.parse(data, offset)
            entries.append(entry)

        self.entries = entries

    def write(self) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(self.index_path)), exist_ok=True)
        # Ensure sorted entries by path
        self.entries.sort(key=lambda e: e.path)

        out = bytearray()
        # Header: DIRC, version 2, entry count
        out.extend(struct.pack(">4sII", b"DIRC", 2, len(self.entries)))

        for e in self.entries:
            out.extend(e.serialize())

        # Trailing 20-byte SHA-1 digest
        checksum = hashlib.sha1(out).digest()
        out.extend(checksum)

        with open(self.index_path, "wb") as f:
            f.write(out)

    def add_entry(self, entry: IndexEntry) -> None:
        # Replace existing entry if path matches
        for idx, e in enumerate(self.entries):
            if e.path == entry.path:
                self.entries[idx] = entry
                return
        self.entries.append(entry)
        self.entries.sort(key=lambda e: e.path)

    def remove_entry(self, path: str) -> None:
        self.entries = [e for e in self.entries if e.path != path]

    def get_entry(self, path: str) -> Optional[IndexEntry]:
        for e in self.entries:
            if e.path == path:
                return e
        return None

    def write_tree(self, git_dir: str) -> str:
        """Converts index entries into hierarchical Tree objects and writes them to the object store.
        Returns the root tree SHA-1.
        """
        # Build nested tree directory structure
        # e.g. root_dict = {"file1": sha, "src": {"code.py": sha}}
        root: dict = {}

        for entry in self.entries:
            parts = entry.path.replace("\\", "/").split("/")
            curr = root
            for part in parts[:-1]:
                if part not in curr:
                    curr[part] = {}
                curr = curr[part]
            # Store file info
            mode_oct = oct(entry.mode)[2:]
            curr[parts[-1]] = (mode_oct, entry.sha)

        def _build_tree(node: dict) -> str:
            tree_entries: List[TreeEntry] = []
            for name, item in node.items():
                if isinstance(item, dict):
                    # Directory -> recurse
                    sub_sha = _build_tree(item)
                    tree_entries.append(TreeEntry(mode="040000", name=name, sha=sub_sha))
                else:
                    mode_oct, sha = item
                    tree_entries.append(TreeEntry(mode=mode_oct, name=name, sha=sha))

            t = Tree(entries=tree_entries)
            return hash_object(git_dir, t, write=True)

        return _build_tree(root)
