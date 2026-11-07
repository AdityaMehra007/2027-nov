from __future__ import annotations
import argparse
import json
from .server import serve
from .engine import WorkflowEngine
from .repository import SQLiteRepository

def main():
    parser = argparse.ArgumentParser(prog="omnia")
    sub = parser.add_subparsers(dest="command", required=True)
    server = sub.add_parser("server")
    server.add_argument("--host", default="127.0.0.1")
    server.add_argument("--port", type=int, default=8765)
    server.add_argument("--db", default="data/omnia.db")
    demo = sub.add_parser("demo")
    demo.add_argument("--db", default="data/omnia.db")
    args = parser.parse_args()
    if args.command == "server":
        serve(args.host, args.port, args.db)
    elif args.command == "demo":
        engine = WorkflowEngine(SQLiteRepository(args.db))
        task = engine.create_task("OMNIA demo task", "demo.echo", "draft",
                                  {"mission": "Turn verified intelligence into safe action"})
        result = engine.execute(task.task_id)
        print(json.dumps(result.to_dict(), indent=2))

if __name__ == "__main__":
    main()
