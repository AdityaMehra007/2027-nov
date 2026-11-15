import os
import tempfile
import unittest
from pygit.diff import compute_diff
from pygit.index import GitIndex, IndexEntry
from pygit.objects import Blob, hash_object
from pygit.repository import init_repo
from pygit.status import get_status

class TestPyGitStatusDiff(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = init_repo(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_status_untracked_and_staged(self):
        # Create a new file on disk
        file1_path = os.path.join(self.repo.worktree, "hello.txt")
        with open(file1_path, "w", encoding="utf-8") as f:
            f.write("line 1\nline 2\n")

        status = get_status(self.repo)
        self.assertIn("hello.txt", status.untracked)
        self.assertEqual(len(status.staged), 0)
        self.assertEqual(len(status.unstaged_modified), 0)

        # Stage the file into index
        blob = Blob(b"line 1\nline 2\n")
        sha = hash_object(self.repo.git_dir, blob, write=True)
        st = os.stat(file1_path)
        index = GitIndex(self.repo.index_path)
        index.add_entry(
            IndexEntry(
                ctime_s=int(st.st_ctime),
                ctime_ns=0,
                mtime_s=int(st.st_mtime),
                mtime_ns=0,
                dev=st.st_dev,
                ino=st.st_ino,
                mode=0o100644,
                uid=st.st_uid,
                gid=st.st_gid,
                file_size=st.st_size,
                sha=sha,
                path="hello.txt",
            )
        )
        index.write()

        status2 = get_status(self.repo)
        self.assertEqual(len(status2.untracked), 0)
        self.assertIn("hello.txt", status2.staged)

        # Modify file on disk without staging
        with open(file1_path, "w", encoding="utf-8") as f:
            f.write("line 1\nline 2 modified\n")

        status3 = get_status(self.repo)
        self.assertIn("hello.txt", status3.unstaged_modified)

        # Test diff
        diff_output = compute_diff(self.repo, "hello.txt")
        self.assertIn("-line 2", diff_output)
        self.assertIn("+line 2 modified", diff_output)

if __name__ == "__main__":
    unittest.main()
