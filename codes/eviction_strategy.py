from abc import ABC, abstractmethod

from codes.cache_entry import CacheEntry, DLLCacheEntry
from codes.data_structure import DLLDataStructure, HeapDataStructure


class EvictionStrategy(ABC):
    @abstractmethod
    def put(self, cache, key, value):
        raise NotImplementedError

    @abstractmethod
    def get(self, cache, key):
        raise NotImplementedError


class LRUEvictionStrategy(EvictionStrategy):

    def __init__(self):
        self.dll = DLLDataStructure()

    def print_state(self):
        return 'DoubleLinkedList(' + repr(self.dll) + ')'

    def put(self, cache, key, value):
        cache_entry = DLLCacheEntry(key, value)

        old_entry = cache.get_from_lookup_dict(key)
        if old_entry is not None:
            cache.pop_from_lookup_dict(key)
            old_entry.disconnect()
            cache.current_size -= 1

        cache.add_to_lookup_dict(key, cache_entry)
        self.dll.add(cache_entry, self.dll.head)
        cache.current_size += 1

        if cache.current_size > cache.capacity:
            tail = cache.pop_from_lookup_dict(self.dll.tail.prev.key)
            tail.disconnect()
            cache.current_size -= 1

    def get(self, cache, key):
        old_entry = cache.get_from_lookup_dict(key)
        if old_entry is None:
            return None
        else:
            old_entry.disconnect()
            self.dll.add(old_entry, self.dll.head)
            return old_entry


class MRUEvictionStrategy(EvictionStrategy):
    def __init__(self):
        self.dll = DLLDataStructure()

    def print_state(self):
        return 'DoubleLinkedList(' + repr(self.dll) + ')'

    def put(self, cache, key, value):
        cache_entry = DLLCacheEntry(key, value)

        old_entry = cache.get_from_lookup_dict(key)
        if old_entry is not None:
            cache.pop_from_lookup_dict(key)
            old_entry.disconnect()
            cache.current_size -= 1

        if cache.current_size == cache.capacity:
            tail = cache.pop_from_lookup_dict(self.dll.tail.prev.key)
            tail.disconnect()
            cache.current_size -= 1

        self.dll.add(cache_entry, self.dll.tail.prev)
        cache.add_to_lookup_dict(key, cache_entry)
        cache.current_size += 1

    def get(self, cache, key):
        old_entry = cache.get_from_lookup_dict(key)
        if old_entry is None:
            return None
        old_entry.disconnect()
        self.dll.add(old_entry, self.dll.tail.prev)
        return old_entry


class SmallestFirstEvictionStrategy(EvictionStrategy):
    def __init__(self):
        self.heap = HeapDataStructure()

    def print_state(self):
        return 'MinHeap(' + repr(self.heap) + ')'

    def put(self, cache, key, value):
        cache_entry = CacheEntry(key, value)

        old_entry = cache.get_from_lookup_dict(key)
        if old_entry is not None:
            old_entry.value = value
        else:
            if cache.current_size == cache.capacity:
                min_cache_entry = self.heap.pop()
                cache.pop_from_lookup_dict(min_cache_entry.key)
                cache.current_size -= 1

            self.heap.push(cache_entry)
            cache.add_to_lookup_dict(key, cache_entry)
            cache.current_size += 1

    def get(self, cache, key):
        return cache.get_from_lookup_dict(key)


