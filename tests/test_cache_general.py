from unittest import TestCase
from codes.cache import Cache


class TestGeneralThings(TestCase):
    def test_key_is_none(self):
        cache = Cache("LRU", 4)
        self.assertRaises(ValueError, cache.put, None, 1)

        cache = Cache("MRU", 4)
        self.assertRaises(ValueError, cache.put, None, 1)

        cache = Cache("SF", 4)
        self.assertRaises(ValueError, cache.put, None, 1)
