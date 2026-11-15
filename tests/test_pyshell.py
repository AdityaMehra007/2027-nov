import io
import os
import tempfile
import unittest
from pyshell.lexer import ShellLexer
from pyshell.parser import ShellParser
from pyshell.executor import ShellExecutor

class TestPyShell(unittest.TestCase):
    def setUp(self):
        self.executor = ShellExecutor()

    def test_lexer_quotes_and_redirection(self):
        lexer = ShellLexer()
        tokens = lexer.tokenize("echo 'hello world' > output.txt")
        self.assertEqual(tokens, ["echo", "hello world", ">", "output.txt"])

        tokens2 = lexer.tokenize('cat "file with spaces.txt" | grep "test" >> log.txt')
        self.assertEqual(tokens2, ["cat", "file with spaces.txt", "|", "grep", "test", ">>", "log.txt"])

    def test_parser_pipeline_and_redirects(self):
        parser = ShellParser()
        cmd_line = parser.parse("cat input.txt | grep foo > result.txt")
        self.assertEqual(len(cmd_line.commands), 2)
        # First command
        self.assertEqual(cmd_line.commands[0].args, ["cat", "input.txt"])
        # Second command
        self.assertEqual(cmd_line.commands[1].args, ["grep", "foo"])
        self.assertEqual(cmd_line.commands[1].stdout_file, "result.txt")
        self.assertFalse(cmd_line.commands[1].stdout_append)

    def test_builtins_execution(self):
        # Echo
        out = self.executor.run_line("echo hello world")
        self.assertEqual(out.strip(), "hello world")

        # Pwd
        out_pwd = self.executor.run_line("pwd")
        self.assertEqual(out_pwd.strip(), os.getcwd())

        # Export & env
        self.executor.run_line("export TEST_VAR=awesome")
        self.assertEqual(self.executor.env.get("TEST_VAR"), "awesome")

    def test_redirection_and_pipes(self):
        with tempfile.TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            os.chdir(tmp)
            try:
                # Write file via redirection
                self.executor.run_line("echo 'sample data' > file.txt")
                self.assertTrue(os.path.exists("file.txt"))
                with open("file.txt", "r") as f:
                    content = f.read().strip()
                self.assertEqual(content, "sample data")

                # Append
                self.executor.run_line("echo 'second line' >> file.txt")
                with open("file.txt", "r") as f:
                    lines = [line.strip() for line in f]
                self.assertEqual(lines, ["sample data", "second line"])
            finally:
                os.chdir(old_cwd)

if __name__ == "__main__":
    unittest.main()
