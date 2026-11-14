import unittest
from pyredis.store import DataStore
from pyredis.commands import CommandDispatcher

class TestCommandDispatcher(unittest.TestCase):
    def setUp(self):
        self.store = DataStore()
        self.dispatcher = CommandDispatcher(self.store)

    def dispatch(self, *parts: str) -> tuple[bytes, bool]:
        raw_args = [p.encode("utf-8") for p in parts]
        return self.dispatcher.dispatch(raw_args)

    def test_connection_commands(self):
        # PING
        res, is_mut = self.dispatch("PING")
        self.assertEqual(res, b"+PONG\r\n")
        self.assertFalse(is_mut)

        res, is_mut = self.dispatch("PING", "custom")
        self.assertEqual(res, b"$6\r\ncustom\r\n")
        self.assertFalse(is_mut)

        # ECHO
        res, is_mut = self.dispatch("ECHO", "hello world")
        self.assertEqual(res, b"$11\r\nhello world\r\n")
        self.assertFalse(is_mut)

        # COMMAND
        res, is_mut = self.dispatch("COMMAND")
        self.assertEqual(res, b"*0\r\n")
        self.assertFalse(is_mut)

        # INFO
        res, is_mut = self.dispatch("INFO")
        self.assertTrue(res.startswith(b"$"))
        self.assertIn(b"redis_version", res)
        self.assertFalse(is_mut)

    def test_strings_commands(self):
        # SET & GET
        res, is_mut = self.dispatch("SET", "mykey", "myval")
        self.assertEqual(res, b"+OK\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("GET", "mykey")
        self.assertEqual(res, b"$5\r\nmyval\r\n")
        self.assertFalse(is_mut)

        # Nonexistent GET
        res, is_mut = self.dispatch("GET", "missing")
        self.assertEqual(res, b"$-1\r\n")
        self.assertFalse(is_mut)

        # SET with EX
        res, is_mut = self.dispatch("SET", "expkey", "expval", "EX", "10")
        self.assertEqual(res, b"+OK\r\n")
        self.assertTrue(is_mut)

        # SET NX fail
        res, is_mut = self.dispatch("SET", "mykey", "newval", "NX")
        self.assertEqual(res, b"$-1\r\n")
        self.assertFalse(is_mut)

        # INCR, DECR, INCRBY
        res, is_mut = self.dispatch("INCR", "num")
        self.assertEqual(res, b":1\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("INCRBY", "num", "5")
        self.assertEqual(res, b":6\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("DECR", "num")
        self.assertEqual(res, b":5\r\n")
        self.assertTrue(is_mut)

        # EXISTS & DEL
        res, is_mut = self.dispatch("EXISTS", "mykey", "num", "missing")
        self.assertEqual(res, b":2\r\n")
        self.assertFalse(is_mut)

        res, is_mut = self.dispatch("DEL", "mykey", "num")
        self.assertEqual(res, b":2\r\n")
        self.assertTrue(is_mut)

    def test_ttl_commands(self):
        self.dispatch("SET", "temp", "val")
        res, is_mut = self.dispatch("EXPIRE", "temp", "60")
        self.assertEqual(res, b":1\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("TTL", "temp")
        self.assertTrue(res.startswith(b":"))
        self.assertFalse(is_mut)

    def test_hash_commands(self):
        res, is_mut = self.dispatch("HSET", "h1", "f1", "v1", "f2", "v2")
        self.assertEqual(res, b":2\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("HGET", "h1", "f1")
        self.assertEqual(res, b"$2\r\nv1\r\n")
        self.assertFalse(is_mut)

        res, is_mut = self.dispatch("HEXISTS", "h1", "f1")
        self.assertEqual(res, b":1\r\n")
        self.assertFalse(is_mut)

        res, is_mut = self.dispatch("HGETALL", "h1")
        self.assertTrue(res.startswith(b"*4\r\n"))
        self.assertFalse(is_mut)

        res, is_mut = self.dispatch("HDEL", "h1", "f1")
        self.assertEqual(res, b":1\r\n")
        self.assertTrue(is_mut)

    def test_list_commands(self):
        res, is_mut = self.dispatch("RPUSH", "l1", "item1", "item2")
        self.assertEqual(res, b":2\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("LPUSH", "l1", "item0")
        self.assertEqual(res, b":3\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("LLEN", "l1")
        self.assertEqual(res, b":3\r\n")
        self.assertFalse(is_mut)

        res, is_mut = self.dispatch("LRANGE", "l1", "0", "-1")
        self.assertTrue(res.startswith(b"*3\r\n"))
        self.assertFalse(is_mut)

        res, is_mut = self.dispatch("LPOP", "l1")
        self.assertEqual(res, b"$5\r\nitem0\r\n")
        self.assertTrue(is_mut)

        res, is_mut = self.dispatch("RPOP", "l1")
        self.assertEqual(res, b"$5\r\nitem2\r\n")
        self.assertTrue(is_mut)

    def test_errors(self):
        # Unknown command
        res, is_mut = self.dispatch("UNKNOWNCOMMAND")
        self.assertTrue(res.startswith(b"-ERR unknown command"))
        self.assertFalse(is_mut)

        # Arity errors
        res, _ = self.dispatch("GET")
        self.assertTrue(res.startswith(b"-ERR wrong number of arguments"))

        res, _ = self.dispatch("SET", "k1")
        self.assertTrue(res.startswith(b"-ERR wrong number of arguments"))

        # Empty args
        res, _ = self.dispatcher.dispatch([])
        self.assertTrue(res.startswith(b"-ERR empty command"))

if __name__ == "__main__":
    unittest.main()
