"""Comprehensive integration and unit test suite for PyGit commands."""

import os
import shutil
import tempfile
import pytest
from pygit.commands import (
    cmd_add,
    cmd_branch,
    cmd_cat_file,
    cmd_checkout,
    cmd_commit,
    cmd_diff_all,
    cmd_hash_object,
    cmd_init,
    cmd_log,
    cmd_status,
    cmd_write_tree,
)
from pygit.repository import find_repo, init_repo


class TestPyGitCommands:
    @pytest.fixture(autouse=True)
    def setup_sandbox(self):
        self.temp_dir = tempfile.mkdtemp(prefix="pygit_test_")
        self.repo = init_repo(self.temp_dir, default_branch="main")
        yield
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_and_find_repo(self):
        assert os.path.exists(os.path.join(self.repo.git_dir, "objects"))
        assert os.path.exists(os.path.join(self.repo.git_dir, "refs", "heads"))
        assert os.path.exists(os.path.join(self.repo.git_dir, "HEAD"))

        # Test finding repo from working directory and nested subdirectory
        found = find_repo(self.temp_dir)
        assert found is not None
        assert found.git_dir == self.repo.git_dir

        nested = os.path.join(self.temp_dir, "a", "b", "c")
        os.makedirs(nested, exist_ok=True)
        found_nested = find_repo(nested)
        assert found_nested is not None
        assert found_nested.git_dir == self.repo.git_dir

    def test_hash_object_and_cat_file(self):
        test_file = os.path.join(self.temp_dir, "hello.txt")
        with open(test_file, "wb") as f:
            f.write(b"Hello, PyGit!\n")

        sha = cmd_hash_object(self.repo.git_dir, test_file, write=True)
        assert len(sha) == 40

        # Read back with cat-file
        content = cmd_cat_file(self.repo.git_dir, sha)
        assert content == "Hello, PyGit!\n"

    def test_add_write_tree_and_commit_workflow(self):
        # Create files
        f1 = os.path.join(self.temp_dir, "file1.txt")
        with open(f1, "w", encoding="utf-8") as f:
            f.write("First file\n")

        sub_dir = os.path.join(self.temp_dir, "sub")
        os.makedirs(sub_dir, exist_ok=True)
        f2 = os.path.join(sub_dir, "file2.txt")
        with open(f2, "w", encoding="utf-8") as f:
            f.write("Second file\n")

        # Add files
        added = cmd_add(self.repo, ["file1.txt", "sub/file2.txt"])
        assert "file1.txt" in added
        assert "sub/file2.txt" in added

        # Write tree
        tree_sha = cmd_write_tree(self.repo)
        assert len(tree_sha) == 40

        # Commit
        commit_sha = cmd_commit(self.repo, message="Initial commit by PyGit")
        assert len(commit_sha) == 40

        # Verify HEAD points to branch pointing to commit
        head_commit = self.repo.get_head_commit()
        assert head_commit == commit_sha

        # Verify log
        logs = cmd_log(self.repo)
        assert len(logs) == 1
        assert logs[0]["sha"] == commit_sha
        assert logs[0]["message"] == "Initial commit by PyGit"

    def test_status_tracking(self):
        f = os.path.join(self.temp_dir, "test.txt")
        with open(f, "w", encoding="utf-8") as file:
            file.write("version 1\n")

        # Initially untracked
        st = cmd_status(self.repo)
        assert "test.txt" in st.untracked

        # After add, it's staged
        cmd_add(self.repo, ["test.txt"])
        st2 = cmd_status(self.repo)
        assert "test.txt" in st2.staged
        assert "test.txt" not in st2.untracked

        # Modify file without staging
        with open(f, "w", encoding="utf-8") as file:
            file.write("version 2 (modified)\n")

        st3 = cmd_status(self.repo)
        assert "test.txt" in st3.unstaged_modified

        # Check diff
        diff = cmd_diff_all(self.repo)
        assert "-version 1" in diff
        assert "+version 2 (modified)" in diff

    def test_branch_and_checkout_lifecycle(self):
        # Initial commit on main
        f = os.path.join(self.temp_dir, "main.txt")
        with open(f, "w", encoding="utf-8") as file:
            file.write("main branch code\n")
        cmd_add(self.repo, ["main.txt"])
        c1 = cmd_commit(self.repo, message="Commit 1 on main")

        # Create branch 'feature'
        branches, curr = cmd_branch(self.repo, name="feature")
        assert "feature" in branches
        assert "main" in branches
        assert curr == "main"

        # Checkout 'feature'
        cmd_checkout(self.repo, "feature")
        assert self.repo.current_branch() == "feature"

        # Make commit on feature
        f_feat = os.path.join(self.temp_dir, "feature.txt")
        with open(f_feat, "w", encoding="utf-8") as file:
            file.write("feature branch code\n")
        cmd_add(self.repo, ["feature.txt"])
        c2 = cmd_commit(self.repo, message="Commit 2 on feature")

        assert self.repo.get_head_commit() == c2
        assert os.path.exists(f_feat)

        # Switch back to 'main'
        cmd_checkout(self.repo, "main")
        assert self.repo.current_branch() == "main"
        assert self.repo.get_head_commit() == c1
        # feature.txt should no longer exist in working tree
        assert not os.path.exists(f_feat)
        assert os.path.exists(f)
