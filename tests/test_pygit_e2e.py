import os
import tempfile
import unittest
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
from pygit.repository import find_repo

class TestPyGitEndToEnd(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.temp_dir.cleanup()

    def test_complete_git_lifecycle(self):
        # 1. Initialize
        repo = cmd_init(".")
        self.assertTrue(os.path.exists(".git"))
        self.assertEqual(repo.current_branch(), "main")

        # 2. Add files
        with open("README.md", "w", encoding="utf-8") as f:
            f.write("# Hello PyGit\nInitial documentation.\n")
        os.makedirs("src", exist_ok=True)
        with open("src/main.py", "w", encoding="utf-8") as f:
            f.write("print('Hello from PyGit')\n")

        # Status: both should be untracked
        st = cmd_status()
        self.assertIn("README.md", st.untracked)
        self.assertIn("src/main.py", st.untracked)

        # Stage both
        cmd_add(["README.md", "src/main.py"])
        st = cmd_status()
        self.assertEqual(len(st.untracked), 0)
        self.assertIn("README.md", st.staged)
        self.assertIn("src/main.py", st.staged)

        # 3. Commit
        commit1_sha = cmd_commit("Initial commit for PyGit")
        self.assertEqual(len(commit1_sha), 40)
        st = cmd_status()
        self.assertEqual(len(st.staged), 0)

        # 4. Check Log
        log_entries = cmd_log()
        self.assertEqual(len(log_entries), 1)
        self.assertEqual(log_entries[0][0], commit1_sha)
        self.assertEqual(log_entries[0][1], "Initial commit for PyGit")

        # 5. Cat-file verification
        cat_content = cmd_cat_file(commit1_sha)
        self.assertIn("Initial commit for PyGit", cat_content)

        # 6. Branching
        cmd_branch("feature/awesome")
        branches = cmd_branch()
        self.assertIn("main", branches)
        self.assertIn("feature/awesome", branches)

        # Switch to feature branch
        cmd_checkout("feature/awesome")
        repo = find_repo()
        self.assertEqual(repo.current_branch(), "feature/awesome")

        # Make modifications on feature branch
        with open("README.md", "a", encoding="utf-8") as f:
            f.write("Awesome new feature added!\n")

        diff_res = cmd_diff("README.md")
        self.assertIn("+Awesome new feature added!", diff_res)

        cmd_add(["README.md"])
        commit2_sha = cmd_commit("Add feature documentation")

        log_feature = cmd_log()
        self.assertEqual(len(log_feature), 2)
        self.assertEqual(log_feature[0][0], commit2_sha)

        # 7. Checkout back to main
        cmd_checkout("main")
        with open("README.md", "r", encoding="utf-8") as f:
            main_readme = f.read()
        # Should not have the awesome line
        self.assertNotIn("Awesome new feature added!", main_readme)

        # Switch back to feature/awesome
        cmd_checkout("feature/awesome")
        with open("README.md", "r", encoding="utf-8") as f:
            feature_readme = f.read()
        self.assertIn("Awesome new feature added!", feature_readme)

if __name__ == "__main__":
    unittest.main()
