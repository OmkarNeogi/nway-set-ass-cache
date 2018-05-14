from unittest import TestCase
from codes.nsacache import NSACache


class TestKVTypeMismatch(TestCase):
    def test_kv_mismatch(self):
        nsac = NSACache(int, int, "MRU", 1, 3)
        nsac.put(1, 1)
        with self.assertRaises(TypeError):
            nsac.put("2", 2)
        with self.assertRaises(TypeError):
            nsac.put(3, "3")
