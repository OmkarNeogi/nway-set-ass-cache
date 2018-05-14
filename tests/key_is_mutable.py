from unittest import TestCase
from codes.nsacache import NSACache


class TestKeyMutable(TestCase):
    def test_key_mutable(self):
        try:
            nsac = NSACache(int, int, "MRU", 1, 3)
        except Exception:
            self.fail('Exception raised unexpectedly.')

        with self.assertRaises(ValueError):
            nsac = NSACache(list, int, "MRU", 1, 3)
        with self.assertRaises(ValueError):
            nsac = NSACache(set, int, "MRU", 1, 3)
