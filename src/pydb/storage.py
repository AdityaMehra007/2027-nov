"""Low-level Paged disk storage and row serialization for PyDB."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os
import struct
from typing import Any, Dict, List, Optional, Set, Tuple


class ColumnType(Enum):
    INTEGER = 1
    TEXT = 2
    REAL = 3

    @classmethod
    def from_str(cls, s: str) -> ColumnType:
        s = s.upper().strip()
        if s in ("INT", "INTEGER"):
            return cls.INTEGER
        elif s in ("TEXT", "VARCHAR", "STRING"):
            return cls.TEXT
        elif s in ("REAL", "FLOAT", "DOUBLE"):
            return cls.REAL
        raise ValueError(f"Unknown column type: {s}")


@dataclass
class Row:
    values: List[Any]


@dataclass
class TableSchema:
    name: str
    columns: List[Tuple[str, ColumnType]]

    def serialize_row(self, row: Row) -> bytes:
        out = bytearray()
        for (_, col_type), val in zip(self.columns, row.values):
            if col_type == ColumnType.INTEGER:
                out.extend(struct.pack(">q", int(val)))
            elif col_type == ColumnType.REAL:
                out.extend(struct.pack(">d", float(val)))
            elif col_type == ColumnType.TEXT:
                encoded = str(val).encode("utf-8")
                out.extend(struct.pack(">H", len(encoded)))
                out.extend(encoded)
        return bytes(out)

    def deserialize_row(self, data: bytes) -> Row:
        values: List[Any] = []
        offset = 0
        for _, col_type in self.columns:
            if col_type == ColumnType.INTEGER:
                val = struct.unpack(">q", data[offset : offset + 8])[0]
                offset += 8
                values.append(val)
            elif col_type == ColumnType.REAL:
                val = struct.unpack(">d", data[offset : offset + 8])[0]
                offset += 8
                values.append(val)
            elif col_type == ColumnType.TEXT:
                str_len = struct.unpack(">H", data[offset : offset + 2])[0]
                offset += 2
                text = data[offset : offset + str_len].decode("utf-8", errors="replace")
                offset += str_len
                values.append(text)
        return Row(values=values)


class Pager:
    def __init__(self, filepath: str, page_size: int = 4096) -> None:
        self.filepath = filepath
        self.page_size = page_size
        self.pages: Dict[int, bytearray] = {}
        self.dirty_pages: Set[int] = set()

        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            self.file = open(filepath, "w+b")
        else:
            self.file = open(filepath, "r+b")

    def num_pages(self) -> int:
        self.file.seek(0, os.SEEK_END)
        file_len = self.file.tell()
        disk_pages = file_len // self.page_size
        if not self.pages:
            return disk_pages
        return max(disk_pages, max(self.pages.keys()) + 1)

    def read_page(self, page_num: int) -> bytearray:
        if page_num in self.pages:
            return self.pages[page_num]

        self.file.seek(page_num * self.page_size)
        data = self.file.read(self.page_size)
        if len(data) < self.page_size:
            # Pad new/short page
            page = bytearray(self.page_size)
            page[: len(data)] = data
        else:
            page = bytearray(data)

        self.pages[page_num] = page
        return page

    def write_page(self, page_num: int, data: bytes) -> None:
        page = bytearray(self.page_size)
        page[: min(len(data), self.page_size)] = data[: self.page_size]
        self.pages[page_num] = page
        self.dirty_pages.add(page_num)

    def flush(self) -> None:
        for page_num in sorted(self.dirty_pages):
            self.file.seek(page_num * self.page_size)
            self.file.write(self.pages[page_num])
        self.file.flush()
        self.dirty_pages.clear()

    def close(self) -> None:
        if hasattr(self, "file") and not self.file.closed:
            self.flush()
            self.file.close()
