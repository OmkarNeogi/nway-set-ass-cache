from unittest import TestCase


class TestMRU(TestCase):
    def test_mru(self):
        from codes.nsacache import NSACache

        nsac = NSACache(int, int, "MRU", 1, 3)
        nsac.put(1, 1)
        nsac.put(2, 2)
        nsac.put(3, 3)
        nsac.put(4, 4)
        nsac.get(2)
        nsac.put(5, 5)
        nsac.put(4, 4)
        nsac.put(6, 6)
        self.assertEqual(str(nsac.caches[0]),
                         "MRUCache("
                         "CacheEntry(1,1),"
                         "CacheEntry(5,5),"
                         "CacheEntry(6,6))")
