"""Append-Only File (AOF) persistence engine for Redis clone."""

from __future__ import annotations
import os
from typing import BinaryIO, Optional, Sequence
from pyredis.protocol import RESPParser, serialize_array
from pyredis.store import DataStore
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from pyredis.commands import CommandDispatcher


class AOFEngine:
    def __init__(self, filepath: str, store: DataStore, dispatcher: CommandDispatcher) -> None:
        self.filepath = filepath
        self.store = store
        self.dispatcher = dispatcher
        self._file: Optional[BinaryIO] = None

    def _ensure_file_open(self) -> BinaryIO:
        if self._file is None or self._file.closed:
            os.makedirs(os.path.dirname(os.path.abspath(self.filepath)), exist_ok=True)
            self._file = open(self.filepath, "ab")
        return self._file

    def append(self, raw_args: Sequence[bytes | str]) -> None:
        """Serializes and appends a mutating command to the AOF log file."""
        resp_bytes = serialize_array(list(raw_args))
        f = self._ensure_file_open()
        f.write(resp_bytes)
        f.flush()

    def replay(self) -> int:
        """Reads the AOF file from disk and executes commands into the DataStore.
        Returns the number of successfully replayed commands.
        """
        if not os.path.exists(self.filepath):
            return 0

        parser = RESPParser()
        replayed_count = 0

        with open(self.filepath, "rb") as f:
            while chunk := f.read(65536):
                parser.feed(chunk)
                while True:
                    cmd_obj = parser.get_next_object()
                    if cmd_obj is None:
                        break
                    if isinstance(cmd_obj, list):
                        self.dispatcher.dispatch(cmd_obj)
                        replayed_count += 1

        return replayed_count

    def close(self) -> None:
        """Flushes and closes the AOF log file."""
        if self._file is not None and not self._file.closed:
            self._file.flush()
            self._file.close()
            self._file = None
