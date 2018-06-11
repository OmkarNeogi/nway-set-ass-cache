from unittest import TestCase
from codes.cache import Cache


class TestSmallestFirstSystem(TestCase):
    def test_smallest_first_system_int_input(self):
        cache = Cache("SF", 3)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        self.assertEqual(cache.get(1), 1)
        self.assertEqual(cache.get(2), 2)
        cache.put(4, 4)
        self.assertEqual(cache.get(1), None)  # evicted (1,1)
        self.assertEqual(cache.get(4), 4)
        cache.put(4, 5)
        self.assertEqual(cache.get(4), 5) # update key 4

    def test_smallest_first_system_str_input(self):
        cache = Cache("SF", 3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        self.assertEqual(cache.get("a"), 1)
        self.assertEqual(cache.get("b"), 2)
        cache.put("d", 4)
        self.assertEqual(cache.get("a"), None)  # evicted ("a",1)
        self.assertEqual(cache.get("d"), 4)

    def test_evicts_smallest(self):
        cache = Cache("SF", 2)
        cache.put((1, 1), 1)
        cache.put((1, 2), 2)
        cache.put((1, 3), 3)
        self.assertEqual(cache.get((1,1)), None)
