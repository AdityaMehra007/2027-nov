"""SQL Lexer and Recursive-Descent Parser for PyDB."""

from __future__ import annotations
from dataclasses import dataclass
import re
from typing import Any, List, Optional, Tuple
from pydb.storage import ColumnType


@dataclass
class WhereClause:
    column: str
    operator: str
    value: Any


@dataclass
class CreateTableStatement:
    table_name: str
    columns: List[Tuple[str, ColumnType]]


@dataclass
class InsertStatement:
    table_name: str
    values: List[Any]


@dataclass
class SelectStatement:
    columns: List[str]  # e.g. ["id", "name"] or ["*"]
    table_name: str
    where: Optional[WhereClause] = None


@dataclass
class DropTableStatement:
    table_name: str


class SQLParser:
    TOKEN_REGEX = re.compile(
        r"""
        (?P<WHITESPACE>\s+)
        |(?P<STRING>'[^']*')
        |(?P<NUMBER>-?\d+(?:\.\d+)?)
        |(?P<OPERATOR><=|>=|!=|<>|<|>|=|LIKE)
        |(?P<PUNCT>[,();*])
        |(?P<IDENT>[a-zA-Z_][a-zA-Z0-9_]*)
        """,
        re.VERBOSE | re.IGNORECASE,
    )

    def tokenize(self, sql: str) -> List[Tuple[str, str]]:
        tokens: List[Tuple[str, str]] = []
        for match in self.TOKEN_REGEX.finditer(sql):
            kind = match.lastgroup
            val = match.group()
            if kind == "WHITESPACE":
                continue
            elif kind == "STRING":
                tokens.append(("STRING", val[1:-1]))
            elif kind == "NUMBER":
                if "." in val:
                    tokens.append(("NUMBER", float(val)))
                else:
                    tokens.append(("NUMBER", int(val)))
            elif kind == "OPERATOR":
                tokens.append(("OPERATOR", val.upper()))
            elif kind == "PUNCT":
                tokens.append(("PUNCT", val))
            elif kind == "IDENT":
                tokens.append(("IDENT", val))
        return tokens

    def parse(self, sql: str) -> Any:
        tokens = self.tokenize(sql)
        if not tokens:
            raise ValueError("Empty SQL statement")

        first_kw = str(tokens[0][1]).upper()
        if first_kw == "CREATE":
            return self._parse_create(tokens)
        elif first_kw == "INSERT":
            return self._parse_insert(tokens)
        elif first_kw == "SELECT":
            return self._parse_select(tokens)
        elif first_kw == "DROP":
            return self._parse_drop(tokens)
        else:
            raise ValueError(f"Unsupported SQL command: {first_kw}")

    def _parse_create(self, tokens: List[Tuple[str, str]]) -> CreateTableStatement:
        # Expected: CREATE TABLE <name> ( col1 type1, col2 type2, ... )
        if len(tokens) < 6 or str(tokens[1][1]).upper() != "TABLE":
            raise ValueError("Syntax error: expected CREATE TABLE <name> (...)")

        table_name = str(tokens[2][1]).lower()
        if tokens[3][1] != "(":
            raise ValueError("Syntax error: expected '(' after table name")

        idx = 4
        columns: List[Tuple[str, ColumnType]] = []
        while idx < len(tokens) and tokens[idx][1] != ")":
            col_name = str(tokens[idx][1]).lower()
            idx += 1
            type_str = str(tokens[idx][1])
            idx += 1
            col_type = ColumnType.from_str(type_str)
            columns.append((col_name, col_type))

            if idx < len(tokens) and tokens[idx][1] == ",":
                idx += 1

        return CreateTableStatement(table_name=table_name, columns=columns)

    def _parse_insert(self, tokens: List[Tuple[str, str]]) -> InsertStatement:
        # Expected: INSERT INTO <name> VALUES ( v1, v2, ... )
        if len(tokens) < 6 or str(tokens[1][1]).upper() != "INTO":
            raise ValueError("Syntax error: expected INSERT INTO <name> VALUES (...)")

        table_name = str(tokens[2][1]).lower()
        if str(tokens[3][1]).upper() != "VALUES" or tokens[4][1] != "(":
            raise ValueError("Syntax error: expected VALUES (...)")

        idx = 5
        values: List[Any] = []
        while idx < len(tokens) and tokens[idx][1] != ")":
            val = tokens[idx][1]
            values.append(val)
            idx += 1
            if idx < len(tokens) and tokens[idx][1] == ",":
                idx += 1

        return InsertStatement(table_name=table_name, values=values)

    def _parse_select(self, tokens: List[Tuple[str, str]]) -> SelectStatement:
        # Expected: SELECT col1, col2 FROM <name> [WHERE col op val]
        idx = 1
        cols: List[str] = []
        while idx < len(tokens) and str(tokens[idx][1]).upper() != "FROM":
            if tokens[idx][1] != ",":
                cols.append(str(tokens[idx][1]).lower())
            idx += 1

        if idx >= len(tokens) or str(tokens[idx][1]).upper() != "FROM":
            raise ValueError("Syntax error: expected FROM in SELECT query")

        idx += 1  # past FROM
        table_name = str(tokens[idx][1]).lower()
        idx += 1

        where: Optional[WhereClause] = None
        if idx < len(tokens) and str(tokens[idx][1]).upper() == "WHERE":
            idx += 1  # past WHERE
            col = str(tokens[idx][1]).lower()
            idx += 1
            op = str(tokens[idx][1]).upper()
            idx += 1
            val = tokens[idx][1]
            where = WhereClause(column=col, operator=op, value=val)

        return SelectStatement(columns=cols, table_name=table_name, where=where)

    def _parse_drop(self, tokens: List[Tuple[str, str]]) -> DropTableStatement:
        # Expected: DROP TABLE <name>
        if len(tokens) < 3 or str(tokens[1][1]).upper() != "TABLE":
            raise ValueError("Syntax error: expected DROP TABLE <name>")
        table_name = str(tokens[2][1]).lower()
        return DropTableStatement(table_name=table_name)
