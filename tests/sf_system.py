from codes.nsacache import NSACache
from unittest import TestCase


class TestSF(TestCase):
    def test_sf(self):
        nsac = NSACache(int, int, "SF", 1, 3)
        nsac.put(1, 1)
        nsac.put(2, 2)
        nsac.put(3, 3)
        nsac.put(4, 4)
        x = nsac.get(2)
        nsac.put(5, 5)
        nsac.put(4, 4)
        nsac.put(6, 6)
        n = nsac.get(10, 5)
        self.assertEqual(str(nsac.caches[0]),
                         "SFCache("
                         "CacheEntry(4,4),"
                         "CacheEntry(5,5),"
                         "CacheEntry(6,6))")
