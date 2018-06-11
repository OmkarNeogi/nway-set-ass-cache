from unittest import TestCase
from codes.nsacache import NSACache


class TestNSACacheSystem(TestCase):
    def test_key_type_mutable(self):
        try:
            nsac = NSACache("MRU", 1, 3, int, int)
        except Exception:
            self.fail('Exception raised unexpectedly.')

        with self.assertRaises(ValueError):
            nsac = NSACache("MRU", 1, 3, list, int)
        with self.assertRaises(ValueError):
            nsac = NSACache("MRU", 1, 3, set, int)

    def test_kv_type_mismatch(self):
        nsac = NSACache("MRU", 1, 3, int, int)
        nsac.put(1, 1)
        with self.assertRaises(TypeError):
            nsac.put("2", 2)
        with self.assertRaises(TypeError):
            nsac.put(3, "3")
