import unittest
from pyredis.protocol import (
    RESPParser,
    RESPError,
    SimpleString,
    serialize_simple_string,
    serialize_error,
    serialize_integer,
    serialize_bulk_string,
    serialize_array,
    serialize_resp,
)


class TestRESPProtocol(unittest.TestCase):
    def test_serialization(self):
        self.assertEqual(serialize_simple_string("OK"), b"+OK\r\n")
        self.assertEqual(serialize_error("ERR unknown"), b"-ERR unknown\r\n")
        self.assertEqual(serialize_integer(42), b":42\r\n")
        self.assertEqual(serialize_bulk_string("hello"), b"$5\r\nhello\r\n")
        self.assertEqual(serialize_bulk_string(b"raw\x00data"), b"$8\r\nraw\x00data\r\n")
        self.assertEqual(serialize_bulk_string(None), b"$-1\r\n")
        self.assertEqual(serialize_array(["GET", "key"]), b"*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n")
        self.assertEqual(serialize_array(None), b"*-1\r\n")

    def test_serialize_resp_types(self):
        self.assertEqual(serialize_resp(SimpleString("OK")), b"+OK\r\n")
        self.assertEqual(serialize_resp("hello"), b"$5\r\nhello\r\n")
        self.assertEqual(serialize_resp(b"binary\x00data"), b"$11\r\nbinary\x00data\r\n")
        self.assertEqual(serialize_resp(123), b":123\r\n")
        self.assertEqual(serialize_resp(-50), b":-50\r\n")
        self.assertEqual(serialize_resp(True), b":1\r\n")
        self.assertEqual(serialize_resp(False), b":0\r\n")
        self.assertEqual(serialize_resp(None), b"$-1\r\n")
        self.assertEqual(serialize_resp(RESPError("ERR invalid")), b"-ERR invalid\r\n")
        self.assertEqual(serialize_resp(Exception("ERR generic")), b"-ERR generic\r\n")
        self.assertEqual(serialize_resp(["SET", "x", 1]), b"*3\r\n$3\r\nSET\r\n$1\r\nx\r\n:1\r\n")
        self.assertEqual(serialize_resp({"k": "v"}), b"*2\r\n$1\r\nk\r\n$1\r\nv\r\n")

    def test_parse_simple_types(self):
        parser = RESPParser()
        parser.feed(b"+PONG\r\n:100\r\n-ERR test\r\n")
        self.assertEqual(parser.get_next_object(), "PONG")
        self.assertEqual(parser.get_next_object(), 100)
        self.assertEqual(parser.get_next_object(), Exception("ERR test"))  # or RESPError
        self.assertIsNone(parser.get_next_object())

    def test_parse_bulk_string(self):
        parser = RESPParser()
        parser.feed(b"$5\r\nworld\r\n$-1\r\n")
        self.assertEqual(parser.get_next_object(), b"world")
        self.assertIsNone(parser.get_next_object())  # null bulk string represented as None

    def test_parse_array(self):
        parser = RESPParser()
        parser.feed(b"*2\r\n$4\r\nECHO\r\n$5\r\nhello\r\n")
        self.assertEqual(parser.get_next_object(), [b"ECHO", b"hello"])

    def test_fragmented_stream(self):
        parser = RESPParser()
        # Feed 1 byte at a time
        full_msg = b"*2\r\n$3\r\nSET\r\n$3\r\nfoo\r\n"
        for byte in full_msg[:-1]:
            parser.feed(bytes([byte]))
            self.assertIsNone(parser.get_next_object())
        parser.feed(bytes([full_msg[-1]]))
        self.assertEqual(parser.get_next_object(), [b"SET", b"foo"])

    def test_empty_and_null_structures(self):
        parser = RESPParser()
        parser.feed(b"*0\r\n$0\r\n\r\n*-1\r\n")
        self.assertEqual(parser.get_next_object(), [])
        self.assertEqual(parser.get_next_object(), b"")
        self.assertIsNone(parser.get_next_object())  # null array -> None
        self.assertIsNone(parser.get_next_object())  # empty buffer -> None

    def test_nested_arrays(self):
        parser = RESPParser()
        parser.feed(b"*2\r\n*2\r\n$1\r\na\r\n$1\r\nb\r\n:99\r\n")
        self.assertEqual(parser.get_next_object(), [[b"a", b"b"], 99])

    def test_get_all_objects(self):
        parser = RESPParser()
        parser.feed(b"+FIRST\r\n:2\r\n$3\r\nFOO\r\n$-1\r\n")
        objs = parser.get_all_objects()
        self.assertEqual(objs, ["FIRST", 2, b"FOO", None])
        self.assertEqual(parser.get_all_objects(), [])

    def test_bulk_string_with_embedded_crlf_and_null_bytes(self):
        parser = RESPParser()
        payload = b"hello\r\nworld\x00\xff!end"
        encoded = serialize_bulk_string(payload)
        parser.feed(encoded)
        parsed = parser.get_next_object()
        self.assertEqual(parsed, payload)

    def test_protocol_errors(self):
        parser = RESPParser()
        parser.feed(b"!invalid\r\n")
        with self.assertRaises(RESPError):
            parser.get_next_object()

        parser = RESPParser()
        parser.feed(b":not_a_number\r\n")
        with self.assertRaises(RESPError):
            parser.get_next_object()

        parser = RESPParser()
        parser.feed(b"$5\r\nhelloNO_CRLF")
        with self.assertRaises(RESPError):
            parser.get_next_object()


if __name__ == "__main__":
    unittest.main()
