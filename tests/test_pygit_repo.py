import os
import tempfile
import unittest
from pygit.repository import GitRepository, find_repo, init_repo

class TestPyGitRepo(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = os.path.join(self.temp_dir.name, "myrepo")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_repo(self):
        repo = init_repo(self.repo_root, default_branch="main")
        self.assertTrue(os.path.exists(repo.git_dir))
        self.assertTrue(os.path.exists(os.path.join(repo.git_dir, "objects")))
        self.assertTrue(os.path.exists(os.path.join(repo.git_dir, "refs", "heads")))

        head_content = repo.get_head_ref()
        self.assertEqual(head_content, "ref: refs/heads/main")
        self.assertIsNone(repo.get_head_commit())

    def test_find_repo_from_nested_subdir(self):
        repo = init_repo(self.repo_root)
        nested = os.path.join(self.repo_root, "a", "b", "c")
        os.makedirs(nested, exist_ok=True)

        found = find_repo(nested)
        self.assertIsNotNone(found)
        self.assertEqual(os.path.abspath(found.worktree), os.path.abspath(self.repo_root))

    def test_branch_refs(self):
        repo = init_repo(self.repo_root)
        dummy_sha = "3b18e512dba79e4c8300dd08aeb37f8e728b8dad"
        repo.update_ref("refs/heads/main", dummy_sha)

        self.assertEqual(repo.get_head_commit(), dummy_sha)
        self.assertEqual(repo.get_ref("refs/heads/main"), dummy_sha)

        # Create another branch
        repo.create_branch("feature", dummy_sha)
        branches = repo.list_branches()
        self.assertIn("main", branches)
        self.assertIn("feature", branches)

if __name__ == "__main__":
    unittest.main()
