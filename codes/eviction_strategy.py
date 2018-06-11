from abc import ABC, abstractmethod

from codes.cache_entry import CacheEntry, DLLCacheEntry
from codes.data_structure import DLLDataStructure, HeapDataStructure


class EvictionStrategy(ABC):
    """Abstract class declaring methods to be overwritten if writing a new
    eviction algorithm."""

    @abstractmethod
    def put(self, cache, key, value):
        """
        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation of
        NSACache
        :param value: Value of type "value_type" specified at instantiation
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, cache, key):
        """
        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation of
        NSACache
        :return: None
        """
        raise NotImplementedError


class LRUEvictionStrategy(EvictionStrategy):

    def __init__(self):
        self.dll = DLLDataStructure()

    def print_state(self):
        return 'DoubleLinkedList(' + repr(self.dll) + ')'

    def put(self, cache, key, value):
        """
        Implements insertion of key-value objects into a cache using the LRU
        eviction strategy in a visitor pattern.
        Brings object to most recently used position.

        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation
        :param value: Value of type "value_type" specified at instantiation
        :return: None
        """
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
        """
        Returns object if exists in cache in an O(1) lookup. Brings object to
        most recently used position.

        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation of
        NSACache
        :return: Key-value object if found in cache, else None
        """
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
        """
        Implements insertion of key-value objects into a cache using the MRU
        eviction strategy in a visitor pattern.
        Brings object to most recently used position.

        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation
        :param value: Value of type "value_type" specified at instantiation
        :return: None
        """
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
        """
        Returns object if exists in cache in an O(1) lookup. Brings object to
        most recently used position.

        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation of
        NSACache
        :return: Key-value object if found in cache, else None
        """
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
        """
        Implements insertion of key-value objects into a cache in a visitor
        pattern.
        Evicts smallest objects first if cache is full.

        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation
        :param value: Value of type "value_type" specified at instantiation
        :return: None
        """
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
        """
        Returns object if exists in cache in an O(1) lookup.

        :param cache: The Cache object to "visit" - perform insertion of
        object on. (Visitor pattern)
        :param key: Key of type "key_type" specified at instantiation of
        NSACache
        :return: Key-value object if found in cache, else None
        """
        return cache.get_from_lookup_dict(key)
