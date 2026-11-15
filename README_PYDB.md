# PyDB: Relational B-Tree Database from Scratch in Python

A lightweight, zero-dependency relational database engine inspired by SQLite, written entirely in Python 3.13 standard library.

---

## Features

- **4KB Paged Disk Storage:** Fixed 4096-byte pages managed by a buffer pool pager, with dirty page caching and atomic sync.
- **Binary Row Serialization:** Compact variable-length and fixed-length data layout for `INTEGER`, `REAL`, and `TEXT` column types.
- **SQL Lexer & Recursive-Descent Parser:** Tokenizes and parses standard DDL and DML SQL statements:
  - `CREATE TABLE <name> (<col> <type>, ...)`
  - `INSERT INTO <name> VALUES (<val>, ...)`
  - `SELECT <cols> FROM <name> [WHERE <col> <op> <val>]`
  - `DROP TABLE <name>`
- **WHERE Filtering:** Evaluates operators `=`, `!=`, `>`, `<`, `>=`, `<=`, and `LIKE`.
- **Interactive REPL & CLI:** SQLite-style CLI with `.tables`, `.schema`, and `.exit` meta-commands.

---

## Quickstart Usage

```bash
# 1. Start interactive REPL
python -m pydb my_database.db

pydb> CREATE TABLE users (id INT, name TEXT, balance REAL);
Table 'users' created successfully

pydb> INSERT INTO users VALUES (1, 'Alice', 250.75);
1 row inserted

pydb> INSERT INTO users VALUES (2, 'Bob', 120.00);
1 row inserted

pydb> SELECT id, name, balance FROM users WHERE balance > 150;
id           | name         | balance     
------------------------------------------
1            | Alice        | 250.75      
(1 rows)

pydb> .tables
users

pydb> .schema users
CREATE TABLE users (id INTEGER, name TEXT, balance REAL);

pydb> .exit
```

---

## Running Tests

```bash
python -m unittest tests/test_pydb_storage.py tests/test_pydb_engine.py
```
```
.....
----------------------------------------------------------------------
Ran 5 tests in 0.244s

OK
```
