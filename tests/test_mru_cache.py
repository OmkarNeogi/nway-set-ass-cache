from unittest import TestCase
from codes.cache import Cache


class TestMRUSystem(TestCase):
    def test_mru_system_int_input(self):

        cache = Cache("MRU", 3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        self.assertEqual(cache.get(1), 1)
        cache.put(4, 4)
        self.assertEqual(cache.get(1), None)  # evicted (1,1)
        self.assertEqual(cache.get(4), 4)
        self.assertEqual(cache.get(3), 3)

    def test_mru_system_tuple_input(self):
        cache = Cache("MRU", 3)
        cache.put((1, 2), 1)
        cache.put((1, 1), 2)
        cache.put((2, 5), 3)
        self.assertEqual(cache.get((1,1)), 2)
        cache.put((5, 6), 4)
        self.assertEqual(cache.get((1, 1)), None)  # evicted ((1,1), 2)
        self.assertEqual(cache.get((0, 0)), None)  # never added
        self.assertEqual(cache.get((5, 6)), 4)
