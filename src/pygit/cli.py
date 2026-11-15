"""CLI entrypoint for PyGit."""

from __future__ import annotations
import argparse
import sys
from pygit.commands import (
    cmd_add,
    cmd_branch,
    cmd_cat_file,
    cmd_checkout,
    cmd_commit,
    cmd_diff,
    cmd_hash_object,
    cmd_init,
    cmd_log,
    cmd_status,
)


def main(args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="pygit", description="PyGit - Zero-dependency Git implementation in Python from Scratch")
    subparsers = parser.add_subparsers(dest="command")

    # init
    p_init = subparsers.add_parser("init", help="Initialize a new empty repository")
    p_init.add_argument("directory", nargs="?", default=".")

    # hash-object
    p_hash = subparsers.add_parser("hash-object", help="Compute object ID and optionally create a blob from a file")
    p_hash.add_argument("-w", "--write", action="store_true", help="Write the object into the object database")
    p_hash.add_argument("file", help="File to hash")

    # cat-file
    p_cat = subparsers.add_parser("cat-file", help="Provide content or type and size information for repository objects")
    p_cat.add_argument("-p", "--pretty", action="store_true", help="Pretty-print the contents of <object>")
    p_cat.add_argument("object", help="Object SHA-1 hash")

    # add
    p_add = subparsers.add_parser("add", help="Add file contents to the index")
    p_add.add_argument("paths", nargs="+", help="Files to add content from")

    # commit
    p_commit = subparsers.add_parser("commit", help="Record changes to the repository")
    p_commit.add_argument("-m", "--message", required=True, help="Commit message")

    # status
    subparsers.add_parser("status", help="Show the working tree status")

    # log
    p_log = subparsers.add_parser("log", help="Show commit logs")
    p_log.add_argument("--oneline", action="store_true", help="Show one line per commit")

    # branch
    p_branch = subparsers.add_parser("branch", help="List, create, or delete branches")
    p_branch.add_argument("name", nargs="?", help="Branch name to create")

    # checkout
    p_checkout = subparsers.add_parser("checkout", help="Switch branches or restore working tree files")
    p_checkout.add_argument("target", help="Branch or commit to switch to")

    # diff
    p_diff = subparsers.add_parser("diff", help="Show changes between commits, commit and working tree, etc")
    p_diff.add_argument("path", nargs="?", help="Specific path to diff")

    parsed = parser.parse_args(args)
    if not parsed.command:
        parser.print_help()
        sys.exit(1)

    try:
        if parsed.command == "init":
            repo = cmd_init(parsed.directory)
            print(f"Initialized empty Git repository in {repo.git_dir}")

        elif parsed.command == "hash-object":
            sha = cmd_hash_object(parsed.file, write=parsed.write)
            print(sha)

        elif parsed.command == "cat-file":
            content = cmd_cat_file(parsed.object)
            print(content, end="" if content.endswith("\n") else "\n")

        elif parsed.command == "add":
            cmd_add(parsed.paths)

        elif parsed.command == "commit":
            sha = cmd_commit(parsed.message)
            print(f"[{sha[:7]}] {parsed.message}")

        elif parsed.command == "status":
            st = cmd_status()
            print("On branch main\n")
            if st.staged:
                print("Changes to be committed:")
                for p in st.staged:
                    print(f"  \033[32mnew file:   {p}\033[0m")
                print()
            if st.unstaged_modified:
                print("Changes not staged for commit:")
                for p in st.unstaged_modified:
                    print(f"  \033[31mmodified:   {p}\033[0m")
                print()
            if st.untracked:
                print("Untracked files:")
                for p in st.untracked:
                    print(f"  \033[31m{p}\033[0m")
                print()
            if not st.staged and not st.unstaged_modified and not st.untracked:
                print("nothing to commit, working tree clean")

        elif parsed.command == "log":
            entries = cmd_log(oneline=parsed.oneline)
            for sha, msg in entries:
                if parsed.oneline:
                    print(f"{sha[:7]} {msg}")
                else:
                    print(f"commit {sha}\n\n    {msg}\n")

        elif parsed.command == "branch":
            res = cmd_branch(parsed.name)
            branches_list, current = res if isinstance(res, tuple) else (res, "main")
            for b in branches_list:
                print(f"* {b}" if b == current else f"  {b}")

        elif parsed.command == "checkout":
            cmd_checkout(parsed.target)
            print(f"Switched to branch '{parsed.target}'")

        elif parsed.command == "diff":
            d = cmd_diff(parsed.path)
            if d:
                print(d, end="")

    except Exception as e:
        print(f"pygit: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
