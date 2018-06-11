from unittest import TestCase
from codes.nsacache import NSACache


class TestNSACacheSystem(TestCase):
    def test_nsacache_system_lru(self):
        nsacache = NSACache("LRU", 2, 3, int, int)

        nsacache.put(1, 1)
        nsacache.put(2, 2)
        nsacache.put(3, 3)
        nsacache.put(4, 4)
        self.assertEqual(nsacache.get(2), 2)
        nsacache.put(5, 5)
        nsacache.put(4, 41)
        nsacache.put(6, 6)
        nsacache.put(7, 7)
        self.assertRaises(KeyError, nsacache.get, 1)
        self.assertEqual(nsacache.get(3), 3)
        nsacache.put(3, 31)
        self.assertEqual(nsacache.get(3), 31)

    def test_nsacache_system_mru(self):
        nsacache = NSACache("LRU", 2, 2, int, int)

        nsacache.put(2, 2)
        nsacache.put(3, 3)
        nsacache.put(1, 1)
        self.assertEqual(nsacache.get(3), 3)
        nsacache.put(4, 4)
        nsacache.put(5, 5)
        self.assertRaises(KeyError, nsacache.get, 1)
        self.assertEqual(nsacache.get(5), 5)

    def test_nsacache_system_sf(self):
        nsacache = NSACache("SF", 2, 2, int, int)

        nsacache.put(1, 1)
        nsacache.put(2, 2)
        nsacache.put(5, 5)
        nsacache.put(4, 4)
        self.assertEqual(nsacache.get(1), 1)
        self.assertEqual(nsacache.get(5), 5)
        nsacache.put(7, 7)
        self.assertEqual(nsacache.get(7), 7)
        self.assertRaises(KeyError, nsacache.get, 1)
