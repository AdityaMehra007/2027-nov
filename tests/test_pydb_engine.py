import os
import tempfile
import unittest
from pydb.engine import DatabaseEngine

class TestPyDBEngine(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "university.db")
        self.engine = DatabaseEngine(self.db_path)

    def tearDown(self):
        self.engine.close()
        self.temp_dir.cleanup()

    def test_create_table_and_insert(self):
        self.engine.execute("CREATE TABLE students (id INT, name TEXT, gpa REAL);")
        tables = self.engine.list_tables()
        self.assertIn("students", tables)

        res1 = self.engine.execute("INSERT INTO students VALUES (1, 'Alice', 3.9);")
        self.assertEqual(res1.rows_affected, 1)

        res2 = self.engine.execute("INSERT INTO students VALUES (2, 'Bob', 3.4);")
        self.assertEqual(res2.rows_affected, 1)

        res3 = self.engine.execute("INSERT INTO students VALUES (3, 'Charlie', 3.8);")
        self.assertEqual(res3.rows_affected, 1)

    def test_select_queries_and_where_filtering(self):
        self.engine.execute("CREATE TABLE products (id INT, title TEXT, price REAL);")
        self.engine.execute("INSERT INTO products VALUES (101, 'Keyboard', 49.99);")
        self.engine.execute("INSERT INTO products VALUES (102, 'Mouse', 19.99);")
        self.engine.execute("INSERT INTO products VALUES (103, 'Monitor', 199.99);")

        # Select all
        res_all = self.engine.execute("SELECT id, title, price FROM products;")
        self.assertEqual(len(res_all.rows), 3)

        # Select with WHERE equality
        res_mouse = self.engine.execute("SELECT title, price FROM products WHERE title = 'Mouse';")
        self.assertEqual(len(res_mouse.rows), 1)
        self.assertEqual(res_mouse.rows[0], ["Mouse", 19.99])

        # Select with WHERE inequality
        res_expensive = self.engine.execute("SELECT id, title FROM products WHERE price > 30;")
        self.assertEqual(len(res_expensive.rows), 2)
        titles = [r[1] for r in res_expensive.rows]
        self.assertIn("Keyboard", titles)
        self.assertIn("Monitor", titles)

    def test_persistence_across_engine_reopen(self):
        self.engine.execute("CREATE TABLE items (id INT, label TEXT);")
        self.engine.execute("INSERT INTO items VALUES (1, 'Alpha');")
        self.engine.execute("INSERT INTO items VALUES (2, 'Beta');")
        self.engine.close()

        # Reopen database
        reopened = DatabaseEngine(self.db_path)
        self.assertIn("items", reopened.list_tables())
        res = reopened.execute("SELECT id, label FROM items;")
        self.assertEqual(len(res.rows), 2)
        self.assertEqual(res.rows[0], [1, "Alpha"])
        self.assertEqual(res.rows[1], [2, "Beta"])
        reopened.close()

if __name__ == "__main__":
    unittest.main()
