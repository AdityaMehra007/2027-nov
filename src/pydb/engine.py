"""Database Engine executing SQL queries over Paged storage for PyDB."""

from __future__ import annotations
from dataclasses import dataclass, field
import json
import os
from typing import Any, Dict, List, Optional
from pydb.parser import (
    CreateTableStatement,
    DropTableStatement,
    InsertStatement,
    SelectStatement,
    SQLParser,
    WhereClause,
)
from pydb.storage import ColumnType, Pager, Row, TableSchema


@dataclass
class QueryResult:
    columns: List[str] = field(default_factory=list)
    rows: List[List[Any]] = field(default_factory=list)
    rows_affected: int = 0
    message: str = ""


class DatabaseEngine:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.pager = Pager(filepath, page_size=4096)
        self.parser = SQLParser()
        self.schemas: Dict[str, TableSchema] = {}
        self.table_pages: Dict[str, List[int]] = {}
        self._load_catalog()

    def _load_catalog(self) -> None:
        """Loads table metadata catalog stored in Page 0."""
        if self.pager.num_pages() == 0:
            return
        p0 = self.pager.read_page(0)
        # First 4 bytes: catalog length
        import struct
        cat_len = struct.unpack(">I", p0[:4])[0]
        if cat_len == 0 or cat_len > 4092:
            return
        try:
            cat_json = p0[4 : 4 + cat_len].decode("utf-8")
            catalog = json.loads(cat_json)
            # catalog = {"tables": {"students": {"columns": [["id", "INT"], ...], "pages": [1, 2]}}}
            for tbl_name, tbl_info in catalog.get("tables", {}).items():
                cols = [(c[0], ColumnType.from_str(c[1])) for c in tbl_info["columns"]]
                self.schemas[tbl_name] = TableSchema(name=tbl_name, columns=cols)
                self.table_pages[tbl_name] = tbl_info.get("pages", [])
        except Exception:
            pass

    def _save_catalog(self) -> None:
        """Saves table metadata catalog into Page 0."""
        catalog: dict = {"tables": {}}
        for tbl_name, schema in self.schemas.items():
            col_list = [[col_name, col_type.name] for col_name, col_type in schema.columns]
            catalog["tables"][tbl_name] = {
                "columns": col_list,
                "pages": self.table_pages.get(tbl_name, []),
            }
        cat_json = json.dumps(catalog).encode("utf-8")
        import struct
        p0 = bytearray(4096)
        p0[:4] = struct.pack(">I", len(cat_json))
        p0[4 : 4 + len(cat_json)] = cat_json
        self.pager.write_page(0, p0)
        self.pager.flush()

    def list_tables(self) -> List[str]:
        return sorted(list(self.schemas.keys()))

    def execute(self, sql: str) -> QueryResult:
        # Strip trailing semicolon
        sql = sql.strip().rstrip(";")
        stmt = self.parser.parse(sql)

        if isinstance(stmt, CreateTableStatement):
            return self._exec_create(stmt)
        elif isinstance(stmt, InsertStatement):
            return self._exec_insert(stmt)
        elif isinstance(stmt, SelectStatement):
            return self._exec_select(stmt)
        elif isinstance(stmt, DropTableStatement):
            return self._exec_drop(stmt)
        else:
            raise ValueError(f"Unknown statement: {stmt}")

    def _exec_create(self, stmt: CreateTableStatement) -> QueryResult:
        if stmt.table_name in self.schemas:
            raise ValueError(f"Table '{stmt.table_name}' already exists")

        schema = TableSchema(name=stmt.table_name, columns=stmt.columns)
        self.schemas[stmt.table_name] = schema
        # Allocate initial page for the table
        new_page_num = max(self.pager.num_pages(), 1)
        # Initialize empty page with 2 bytes count = 0
        init_page = bytearray(4096)
        self.pager.write_page(new_page_num, init_page)
        self.table_pages[stmt.table_name] = [new_page_num]

        self._save_catalog()
        return QueryResult(message=f"Table '{stmt.table_name}' created successfully")

    def _exec_insert(self, stmt: InsertStatement) -> QueryResult:
        schema = self.schemas.get(stmt.table_name)
        if not schema:
            raise ValueError(f"Table '{stmt.table_name}' does not exist")

        if len(stmt.values) != len(schema.columns):
            raise ValueError(
                f"Column count mismatch: expected {len(schema.columns)} values, got {len(stmt.values)}"
            )

        row = Row(values=stmt.values)
        payload = schema.serialize_row(row)

        pages = self.table_pages.get(stmt.table_name, [])
        if not pages:
            new_p = max(self.pager.num_pages(), 1)
            pages.append(new_p)
            self.table_pages[stmt.table_name] = pages

        # Find page with space
        import struct
        inserted = False
        for p_num in pages:
            page = self.pager.read_page(p_num)
            row_count, free_offset = struct.unpack(">HH", page[:4])
            if free_offset == 0:
                free_offset = 4

            # 2 bytes row length + row payload
            space_needed = 2 + len(payload)
            if free_offset + space_needed <= 4096:
                # Append row
                page[free_offset : free_offset + 2] = struct.pack(">H", len(payload))
                page[free_offset + 2 : free_offset + space_needed] = payload
                free_offset += space_needed
                row_count += 1
                page[:4] = struct.pack(">HH", row_count, free_offset)
                self.pager.write_page(p_num, page)
                inserted = True
                break

        if not inserted:
            # Allocate new page
            new_p = max(self.pager.num_pages(), 1)
            pages.append(new_p)
            page = bytearray(4096)
            space_needed = 2 + len(payload)
            page[4 : 4 + 2] = struct.pack(">H", len(payload))
            page[6 : 4 + space_needed] = payload
            page[:4] = struct.pack(">HH", 1, 4 + space_needed)
            self.pager.write_page(new_p, page)

        self._save_catalog()
        return QueryResult(rows_affected=1, message="1 row inserted")

    def _exec_select(self, stmt: SelectStatement) -> QueryResult:
        schema = self.schemas.get(stmt.table_name)
        if not schema:
            raise ValueError(f"Table '{stmt.table_name}' does not exist")

        # Resolve selected columns
        all_col_names = [col[0] for col in schema.columns]
        if stmt.columns == ["*"]:
            selected_cols = all_col_names
            col_indices = list(range(len(all_col_names)))
        else:
            selected_cols = stmt.columns
            col_indices = []
            for c in selected_cols:
                if c not in all_col_names:
                    raise ValueError(f"Column '{c}' not found in table '{stmt.table_name}'")
                col_indices.append(all_col_names.index(c))

        # Read rows from all table pages
        import struct
        matched_rows: List[List[Any]] = []
        pages = self.table_pages.get(stmt.table_name, [])

        for p_num in pages:
            page = self.pager.read_page(p_num)
            row_count, free_offset = struct.unpack(">HH", page[:4])
            if row_count == 0:
                continue

            offset = 4
            for _ in range(row_count):
                row_len = struct.unpack(">H", page[offset : offset + 2])[0]
                offset += 2
                row_bytes = page[offset : offset + row_len]
                offset += row_len

                row = schema.deserialize_row(row_bytes)

                # Check WHERE condition
                if stmt.where:
                    where_col_idx = all_col_names.index(stmt.where.column)
                    col_val = row.values[where_col_idx]
                    target_val = stmt.where.value
                    op = stmt.where.operator

                    if op == "=" and not (col_val == target_val):
                        continue
                    elif op in ("!=", "<>") and not (col_val != target_val):
                        continue
                    elif op == ">" and not (col_val > target_val):
                        continue
                    elif op == "<" and not (col_val < target_val):
                        continue
                    elif op == ">=" and not (col_val >= target_val):
                        continue
                    elif op == "<=" and not (col_val <= target_val):
                        continue
                    elif op == "LIKE":
                        import fnmatch
                        pat = str(target_val).replace("%", "*").replace("_", "?")
                        if not fnmatch.fnmatch(str(col_val), pat):
                            continue

                filtered_values = [row.values[i] for i in col_indices]
                matched_rows.append(filtered_values)

        return QueryResult(columns=selected_cols, rows=matched_rows)

    def _exec_drop(self, stmt: DropTableStatement) -> QueryResult:
        if stmt.table_name not in self.schemas:
            raise ValueError(f"Table '{stmt.table_name}' does not exist")
        del self.schemas[stmt.table_name]
        self.table_pages.pop(stmt.table_name, None)
        self._save_catalog()
        return QueryResult(message=f"Table '{stmt.table_name}' dropped successfully")

    def close(self) -> None:
        if hasattr(self, "pager"):
            self.pager.close()
