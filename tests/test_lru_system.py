from codes.nsacache import NSACache
from unittest import TestCase


class TestLRU(TestCase):
    def test_lru1(self):
        nsac = NSACache(int, int, "LRU", 1, 3)
        nsac.put(1, 1)
        nsac.put(2, 2)
        nsac.put(3, 3)
        nsac.put(4, 4)
        nsac.get(2)
        nsac.put(5, 5)
        nsac.put(4, 4)
        nsac.put(6, 6)
        self.assertEqual(str(nsac.caches[0]),
                         "LRUCache("
                         "CacheEntry(6,6),"
                         "CacheEntry(4,4),"
                         "CacheEntry(5,5))")
