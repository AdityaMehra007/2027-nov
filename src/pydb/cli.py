"""CLI and interactive REPL for PyDB."""

from __future__ import annotations
import argparse
import sys
from pydb.engine import DatabaseEngine


def run_repl(db_path: str) -> None:
    engine = DatabaseEngine(db_path)
    print(f"PyDB v0.1.0 - Connected to {db_path}")
    print("Enter \".help\" for usage hints, \".exit\" to quit.\n")

    while True:
        try:
            line = input("pydb> ").strip()
            if not line:
                continue

            if line.startswith("."):
                cmd = line.lower()
                if cmd in (".exit", ".quit"):
                    break
                elif cmd == ".tables":
                    tables = engine.list_tables()
                    print("  ".join(tables) if tables else "No tables found.")
                elif cmd.startswith(".schema"):
                    parts = line.split(maxsplit=1)
                    if len(parts) == 2:
                        tbl = parts[1]
                        schema = engine.schemas.get(tbl)
                        if schema:
                            cols = [f"{c[0]} {c[1].name}" for c in schema.columns]
                            print(f"CREATE TABLE {tbl} ({', '.join(cols)});")
                        else:
                            print(f"Table '{tbl}' not found.")
                    else:
                        for tbl, schema in engine.schemas.items():
                            cols = [f"{c[0]} {c[1].name}" for c in schema.columns]
                            print(f"CREATE TABLE {tbl} ({', '.join(cols)});")
                elif cmd == ".help":
                    print(".tables            List names of tables")
                    print(".schema [table]    Show CREATE statements")
                    print(".exit              Exit this program")
                else:
                    print(f"Error: unknown command: {line}")
                continue

            # Execute SQL
            res = engine.execute(line)
            if res.columns:
                # Format table
                header = " | ".join(f"{c:<12}" for c in res.columns)
                print(header)
                print("-" * len(header))
                for r in res.rows:
                    print(" | ".join(f"{str(v):<12}" for v in r))
                print(f"({len(res.rows)} rows)\n")
            elif res.message:
                print(res.message)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting PyDB.")
            break
        except Exception as e:
            print(f"Error: {e}")

    engine.close()


def main() -> None:
    parser = argparse.ArgumentParser(prog="pydb", description="PyDB - Relational B-Tree Database from Scratch")
    parser.add_argument("database", nargs="?", default="pydb.db", help="Path to database file (default: pydb.db)")
    parser.add_argument("-c", "--command", help="Execute single SQL statement and exit")

    args = parser.parse_args()

    if args.command:
        engine = DatabaseEngine(args.database)
        try:
            res = engine.execute(args.command)
            if res.columns:
                print(" | ".join(res.columns))
                for r in res.rows:
                    print(" | ".join(str(v) for v in r))
            elif res.message:
                print(res.message)
        finally:
            engine.close()
    else:
        run_repl(args.database)


if __name__ == "__main__":
    main()
