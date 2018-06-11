from unittest import TestCase
from codes.cache import Cache


class TestLRUSystem(TestCase):
    def test_lru_system_int_input(self):

        cache = Cache("LRU", 3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        self.assertEqual(cache.get(1), 1)
        cache.put(4, 4)
        self.assertEqual(cache.get(2), None)  # evicted (2,2)
        self.assertEqual(cache.get(4), 4)

    def test_lru_system_tuple_input(self):
        cache = Cache("LRU", 3)
        cache.put((1, 2), 1)
        cache.put((1, 1), 2)
        cache.put((2, 5), 3)
        self.assertEqual(cache.get((1,1)), 2)
        cache.put((5, 6), 4)
        self.assertEqual(cache.get((1, 2)), None)  # evicted ((1,2), 1)
        self.assertEqual(cache.get((0, 0)), None)
        self.assertEqual(cache.get((2, 5)), 3)
