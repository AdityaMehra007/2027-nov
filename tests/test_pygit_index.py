import os
import tempfile
import unittest
from pygit.index import GitIndex, IndexEntry
from pygit.objects import Blob, Tree, hash_object, read_object

class TestPyGitIndex(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.git_dir = os.path.join(self.temp_dir.name, ".git")
        os.makedirs(os.path.join(self.git_dir, "objects"), exist_ok=True)
        self.index_path = os.path.join(self.git_dir, "index")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_empty_index_read_and_write(self):
        index = GitIndex(self.index_path)
        index.write()

        self.assertTrue(os.path.exists(self.index_path))
        # Header is 12 bytes + 20 bytes checksum = 32 bytes
        self.assertEqual(os.path.getsize(self.index_path), 32)

        # Read back
        loaded = GitIndex(self.index_path)
        loaded.read()
        self.assertEqual(len(loaded.entries), 0)

    def test_add_entries_and_roundtrip(self):
        index = GitIndex(self.index_path)
        sha1 = "3b18e512dba79e4c8300dd08aeb37f8e728b8dad"
        entry1 = IndexEntry(
            ctime_s=1700000000,
            ctime_ns=0,
            mtime_s=1700000001,
            mtime_ns=0,
            dev=1,
            ino=2,
            mode=0o100644,
            uid=1000,
            gid=1000,
            file_size=12,
            sha=sha1,
            path="file1.txt",
        )
        entry2 = IndexEntry(
            ctime_s=1700000000,
            ctime_ns=0,
            mtime_s=1700000002,
            mtime_ns=0,
            dev=1,
            ino=3,
            mode=0o100644,
            uid=1000,
            gid=1000,
            file_size=20,
            sha=sha1,
            path="docs/guide.md",
        )
        index.add_entry(entry1)
        index.add_entry(entry2)
        index.write()

        # Read back and verify entries are sorted and matching
        loaded = GitIndex(self.index_path)
        loaded.read()
        self.assertEqual(len(loaded.entries), 2)
        paths = [e.path for e in loaded.entries]
        self.assertEqual(paths, ["docs/guide.md", "file1.txt"])
        self.assertEqual(loaded.entries[0].sha, sha1)

    def test_write_tree_hierarchical(self):
        index = GitIndex(self.index_path)
        # Create blobs
        b1 = Blob(b"file at root")
        b2 = Blob(b"file in sub")
        sha1 = hash_object(self.git_dir, b1, write=True)
        sha2 = hash_object(self.git_dir, b2, write=True)

        e1 = IndexEntry(0, 0, 0, 0, 0, 0, 0o100644, 0, 0, len(b1.data), sha1, "root.txt")
        e2 = IndexEntry(0, 0, 0, 0, 0, 0, 0o100644, 0, 0, len(b2.data), sha2, "src/code.py")
        index.add_entry(e1)
        index.add_entry(e2)

        root_tree_sha = index.write_tree(self.git_dir)
        self.assertIsNotNone(root_tree_sha)

        # Inspect root tree
        root_tree = read_object(self.git_dir, root_tree_sha)
        self.assertIsInstance(root_tree, Tree)
        names = [entry.name for entry in root_tree.entries]
        self.assertIn("root.txt", names)
        self.assertIn("src", names)

        # Inspect sub tree
        src_entry = next(entry for entry in root_tree.entries if entry.name == "src")
        self.assertEqual(src_entry.mode, "040000")
        src_tree = read_object(self.git_dir, src_entry.sha)
        self.assertIsInstance(src_tree, Tree)
        self.assertEqual(src_tree.entries[0].name, "code.py")

if __name__ == "__main__":
    unittest.main()
