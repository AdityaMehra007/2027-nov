import os
import tempfile
import unittest
from pyredis.commands import CommandDispatcher
from pyredis.persistence import AOFEngine
from pyredis.store import DataStore

class TestAOFPersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.aof_path = os.path.join(self.temp_dir.name, "test_appendonly.aof")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_aof_append_and_replay(self):
        store = DataStore()
        dispatcher = CommandDispatcher(store)
        aof = AOFEngine(self.aof_path, store, dispatcher)

        # Mutating operations
        aof.append([b"SET", b"name", b"RedisClone"])
        aof.append([b"HSET", b"user:100", b"role", b"admin", b"active", b"true"])
        aof.append([b"RPUSH", b"queue", b"task1", b"task2"])
        aof.append([b"INCR", b"visitors"])
        aof.close()

        self.assertTrue(os.path.exists(self.aof_path))
        self.assertGreater(os.path.getsize(self.aof_path), 0)

        # Replay into fresh store
        fresh_store = DataStore()
        fresh_dispatcher = CommandDispatcher(fresh_store)
        recovery_aof = AOFEngine(self.aof_path, fresh_store, fresh_dispatcher)

        count = recovery_aof.replay()
        recovery_aof.close()

        self.assertEqual(count, 4)
        # Verify restored state
        self.assertEqual(fresh_store.get("name"), "RedisClone")
        self.assertEqual(fresh_store.hgetall("user:100"), {"role": "admin", "active": "true"})
        self.assertEqual(fresh_store.lrange("queue", 0, -1), ["task1", "task2"])
        self.assertEqual(fresh_store.get("visitors"), "1")

    def test_aof_empty_or_missing(self):
        store = DataStore()
        dispatcher = CommandDispatcher(store)
        missing_path = os.path.join(self.temp_dir.name, "missing.aof")
        aof = AOFEngine(missing_path, store, dispatcher)
        count = aof.replay()
        aof.close()
        self.assertEqual(count, 0)

if __name__ == "__main__":
    unittest.main()
