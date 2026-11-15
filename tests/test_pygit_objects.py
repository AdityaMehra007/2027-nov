import os
import tempfile
import unittest
from pygit.objects import (
    Blob,
    Commit,
    GitObject,
    Tree,
    TreeEntry,
    hash_object,
    read_object,
)

class TestPyGitObjects(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.git_dir = os.path.join(self.temp_dir.name, ".git")
        os.makedirs(os.path.join(self.git_dir, "objects"), exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_blob_serialization_and_hashing(self):
        content = b"hello world\n"
        blob = Blob(content)
        # Expected git hash: sha1("blob 12\x00hello world\n") -> 3b18e512dba79e4c8300dd08aeb37f8e728b8dad
        sha = blob.sha1()
        self.assertEqual(sha, "3b18e512dba79e4c8300dd08aeb37f8e728b8dad")

        # Write to disk and read back
        written_sha = hash_object(self.git_dir, blob, write=True)
        self.assertEqual(written_sha, sha)

        # Check object file exists at .git/objects/3b/18e512...
        obj_file = os.path.join(self.git_dir, "objects", sha[:2], sha[2:])
        self.assertTrue(os.path.exists(obj_file))

        # Read back
        loaded = read_object(self.git_dir, sha)
        self.assertIsInstance(loaded, Blob)
        self.assertEqual(loaded.data, content)

    def test_tree_serialization_and_parsing(self):
        # Create tree with two entries: one file and one subfolder
        file_sha = "3b18e512dba79e4c8300dd08aeb91964250bc328"
        dir_sha = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # empty tree sha in git

        entry1 = TreeEntry(mode="100644", name="hello.txt", sha=file_sha)
        entry2 = TreeEntry(mode="040000", name="subdir", sha=dir_sha)

        tree = Tree(entries=[entry1, entry2])
        sha = hash_object(self.git_dir, tree, write=True)

        loaded_tree = read_object(self.git_dir, sha)
        self.assertIsInstance(loaded_tree, Tree)
        self.assertEqual(len(loaded_tree.entries), 2)
        self.assertEqual(loaded_tree.entries[0].name, "hello.txt")
        self.assertEqual(loaded_tree.entries[0].sha, file_sha)
        self.assertEqual(loaded_tree.entries[1].name, "subdir")
        self.assertEqual(loaded_tree.entries[1].sha, dir_sha)

    def test_commit_serialization_and_parsing(self):
        tree_sha = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
        commit = Commit(
            tree_sha=tree_sha,
            parent_shas=[],
            author="Aditya Mehra <aditya@example.com> 1700000000 +0000",
            committer="Aditya Mehra <aditya@example.com> 1700000000 +0000",
            message="Initial commit\n",
        )
        sha = hash_object(self.git_dir, commit, write=True)

        loaded_commit = read_object(self.git_dir, sha)
        self.assertIsInstance(loaded_commit, Commit)
        self.assertEqual(loaded_commit.tree_sha, tree_sha)
        self.assertEqual(loaded_commit.parent_shas, [])
        self.assertIn("Initial commit", loaded_commit.message)

if __name__ == "__main__":
    unittest.main()
