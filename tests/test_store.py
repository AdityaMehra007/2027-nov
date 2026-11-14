import time
import unittest
from pyredis.store import DataStore, WrongTypeError

class TestDataStore(unittest.TestCase):
    def setUp(self):
        self.store = DataStore()

    def test_strings_basic(self):
        self.assertTrue(self.store.set("k1", "v1"))
        self.assertEqual(self.store.get("k1"), "v1")
        self.assertIsNone(self.store.get("nonexistent"))
        self.assertEqual(self.store.exists("k1", "nonexistent"), 1)
        self.assertEqual(self.store.delete("k1", "k2"), 1)
        self.assertIsNone(self.store.get("k1"))

    def test_strings_nx_xx(self):
        # NX: only set if not exists
        self.assertTrue(self.store.set("foo", "bar", nx=True))
        self.assertFalse(self.store.set("foo", "baz", nx=True))
        self.assertEqual(self.store.get("foo"), "bar")

        # XX: only set if exists
        self.assertFalse(self.store.set("other", "val", xx=True))
        self.assertTrue(self.store.set("foo", "new_bar", xx=True))
        self.assertEqual(self.store.get("foo"), "new_bar")

    def test_incr_decr(self):
        self.assertEqual(self.store.incr_by("counter", 1), 1)
        self.assertEqual(self.store.incr_by("counter", 5), 6)
        self.assertEqual(self.store.incr_by("counter", -2), 4)
        self.assertEqual(self.store.get("counter"), "4")

        self.store.set("str_val", "not_a_number")
        with self.assertRaises(ValueError):
            self.store.incr_by("str_val", 1)

    def test_ttl_and_passive_expiration(self):
        # Set with EX (seconds)
        self.store.set("temp", "val", ex_sec=0.05)
        self.assertEqual(self.store.get("temp"), "val")
        self.assertGreater(self.store.ttl("temp"), 0)
        self.assertGreater(self.store.pttl("temp"), 0)

        time.sleep(0.06)
        # Passive eviction on access
        self.assertIsNone(self.store.get("temp"))
        self.assertEqual(self.store.ttl("temp"), -2)
        self.assertEqual(self.store.pttl("temp"), -2)

    def test_expire_and_pexpire(self):
        self.store.set("persisted", "data")
        self.assertEqual(self.store.ttl("persisted"), -1)
        self.assertTrue(self.store.expire("persisted", 10))
        self.assertGreater(self.store.ttl("persisted"), 0)

        self.assertTrue(self.store.pexpire("persisted", 50))
        time.sleep(0.06)
        self.assertEqual(self.store.exists("persisted"), 0)

    def test_hashes(self):
        # HSET & HGET
        added = self.store.hset("user:1", {"name": "Alice", "role": "admin"})
        self.assertEqual(added, 2)
        self.assertEqual(self.store.hget("user:1", "name"), "Alice")
        self.assertIsNone(self.store.hget("user:1", "missing"))
        self.assertTrue(self.store.hexists("user:1", "name"))
        self.assertFalse(self.store.hexists("user:1", "missing"))

        # HGETALL
        all_data = self.store.hgetall("user:1")
        self.assertEqual(all_data, {"name": "Alice", "role": "admin"})

        # HDEL
        self.assertEqual(self.store.hdel("user:1", "role", "other"), 1)
        self.assertEqual(self.store.hgetall("user:1"), {"name": "Alice"})

    def test_lists(self):
        # LPUSH / RPUSH
        self.assertEqual(self.store.rpush("mylist", "a", "b"), 2)
        self.assertEqual(self.store.lpush("mylist", "z"), 3)
        self.assertEqual(self.store.llen("mylist"), 3)

        # LRANGE
        self.assertEqual(self.store.lrange("mylist", 0, -1), ["z", "a", "b"])
        self.assertEqual(self.store.lrange("mylist", 1, 2), ["a", "b"])
        self.assertEqual(self.store.lrange("mylist", 0, 0), ["z"])

        # LPOP / RPOP
        self.assertEqual(self.store.lpop("mylist", 1), ["z"])
        self.assertEqual(self.store.rpop("mylist", 1), ["b"])
        self.assertEqual(self.store.llen("mylist"), 1)
        self.assertEqual(self.store.lrange("mylist", 0, -1), ["a"])

    def test_wrong_type_error(self):
        self.store.set("str_key", "string_val")
        with self.assertRaises(WrongTypeError):
            self.store.hget("str_key", "field")
        with self.assertRaises(WrongTypeError):
            self.store.lpush("str_key", "item")

        self.store.hset("hash_key", {"f1": "v1"})
        with self.assertRaises(WrongTypeError):
            self.store.get("hash_key")
        with self.assertRaises(WrongTypeError):
            self.store.rpop("hash_key")

    def test_keys_and_flushdb(self):
        self.store.set("app:user:1", "u1")
        self.store.set("app:user:2", "u2")
        self.store.set("sys:config", "cfg")

        keys = sorted(self.store.keys("app:*"))
        self.assertEqual(keys, ["app:user:1", "app:user:2"])
        all_keys = sorted(self.store.keys("*"))
        self.assertEqual(all_keys, ["app:user:1", "app:user:2", "sys:config"])

        self.store.flushdb()
        self.assertEqual(self.store.keys("*"), [])

if __name__ == "__main__":
    unittest.main()
