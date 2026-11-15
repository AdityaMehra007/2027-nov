import os
import tempfile
import unittest
from pydb.storage import Pager, Row, TableSchema, ColumnType

class TestPyDBStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test.db")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_pager_write_and_read_pages(self):
        pager = Pager(self.db_path, page_size=4096)
        page0 = bytearray(4096)
        page0[:10] = b"HELLO_DB_0"
        pager.write_page(0, bytes(page0))

        page1 = bytearray(4096)
        page1[:10] = b"HELLO_DB_1"
        pager.write_page(1, bytes(page1))
        pager.flush()
        pager.close()

        # Reopen and read
        pager2 = Pager(self.db_path, page_size=4096)
        r0 = pager2.read_page(0)
        r1 = pager2.read_page(1)
        self.assertEqual(r0[:10], b"HELLO_DB_0")
        self.assertEqual(r1[:10], b"HELLO_DB_1")
        self.assertEqual(pager2.num_pages(), 2)
        pager2.close()

    def test_row_serialization_and_deserialization(self):
        schema = TableSchema(
            name="users",
            columns=[
                ("id", ColumnType.INTEGER),
                ("username", ColumnType.TEXT),
                ("score", ColumnType.REAL),
            ],
        )

        row = Row(values=[1, "alice", 98.5])
        payload = schema.serialize_row(row)

        deserialized = schema.deserialize_row(payload)
        self.assertEqual(deserialized.values, [1, "alice", 98.5])

if __name__ == "__main__":
    unittest.main()
