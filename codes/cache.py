from abc import ABC, abstractmethod


class Cache(ABC):
    """
    Abstract class for other Caches to inherit from.
    Implements only the dictionary lookup and manipulation methods which are
    shared across child classes
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.current_size = 0
        self.key_lookup = {}

    def pop_from_lookup_dict(self, key):
        return self.key_lookup.pop(key, None)

    def add_to_lookup_dict(self, key, to_add):
        self.key_lookup[key] = to_add

    def exists_in_lookup_dict(self, key):
        return key in self.key_lookup

    def get_from_lookup_dict(self, key):
        return self.key_lookup.get(key, None)

    @abstractmethod
    def put(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass


class LRUCache(Cache):
    """An implementation of the least recently utilised eviction strategy"""

    def __init__(self, capacity):
        from codes.data_structure import DLLDataStructure
        super().__init__(capacity)

        self.data_structure = DLLDataStructure()

    def put(self, key, value):
        """
        Make a DLLCacheEntry from key and value, then add to cache if
        it does not exist already. If it exists, bring to most recently
        used position in cache.
        If size exceeds capacity, remove oldest element.

        :param key: an immutable key
        :param value: an arbitrarily typed value
        :return: None
        """
        from codes.cache_entry import DLLCacheEntry
        cache_entry = DLLCacheEntry(key, value)

        old_cache_entry = self.get_from_lookup_dict(key)
        if old_cache_entry is not None:
            self.pop_from_lookup_dict(key)
            old_cache_entry.disconnect()
            self.current_size -= 1

        self.add_to_lookup_dict(key, cache_entry)
        self.data_structure.dll_add(cache_entry, self.data_structure.head)
        self.current_size += 1

        if self.current_size > self.capacity:
            tail = self.pop_from_lookup_dict(self.data_structure.tail.prev.key)
            tail.disconnect()
            self.current_size -= 1

    def get(self, key):
        """
        Get if available in cache through amortized O(1) lookup.
        If available, bring to most recently used position in cache.
        Returns None if key not in cache.

        :param key: an immutable key
        :return: a DLLCacheEntry object or None
        """
        old_cache_entry = self.get_from_lookup_dict(key)
        if old_cache_entry is None:
            return None
        old_cache_entry.disconnect()
        self.data_structure.dll_add(old_cache_entry, self.data_structure.head)
        return old_cache_entry

    def __repr__(self):
        return "LRUCache(" \
               + ','.join([str(cache_ent)
                           for cache_ent in self.data_structure]) \
               + ")"


class MRUCache(Cache):
    """An implementation of the most recently used eviction strategy"""

    def __init__(self, capacity):
        from codes.data_structure import DLLDataStructure
        super().__init__(capacity)

        self.data_structure = DLLDataStructure()

    def put(self, key, value):
        """
        Make a DLLCacheEntry from key and value, then add to cache if it does
        not exist already. If it does, bring to most recently used position in
        cache.
        If size exceeds capacity, replace most recently accessed element with
        new DLLCacheEntry.

        :param key: an immutable key
        :param value: an arbitrarily typed value
        :return: None
        """
        from codes.cache_entry import DLLCacheEntry
        cache_entry = DLLCacheEntry(key, value)

        old_cache_entry = self.get_from_lookup_dict(key)
        if old_cache_entry is not None:
            self.pop_from_lookup_dict(key)
            old_cache_entry.disconnect()
            self.current_size -= 1

        if self.current_size == self.capacity:
            tail = self.pop_from_lookup_dict(self.data_structure.tail.prev.key)
            tail.disconnect()
            self.current_size -= 1

        self.add_to_lookup_dict(key, cache_entry)
        self.data_structure.dll_add(cache_entry, self.data_structure.tail.prev)
        self.current_size += 1

    def get(self, key):
        """
        Get if available in cache through amortized O(1) lookup.
        If available, bring to most recently used position in cache.
        Returns None if key not in cache.

        :param key: an immutable key
        :return: a DLLCacheEntry object or None
        """
        old_cache_entry = self.get_from_lookup_dict(key)
        if old_cache_entry is None:
            return None
        old_cache_entry.disconnect()
        self.data_structure.dll_add(old_cache_entry,
                                    self.data_structure.tail.prev)
        return old_cache_entry

    def __repr__(self):
        return "MRUCache(" \
               + ','.join([str(cache_ent)
                           for cache_ent in self.data_structure]) \
               + ")"


class SFCache(Cache):
    """An implementation of the smallest key first eviction strategy"""

    def __init__(self, capacity):
        from codes.data_structure import MinHeapDataStructure
        super().__init__(capacity)

        self.data_structure = MinHeapDataStructure()

    def put(self, key, value):
        """
        Make a SFCacheEntry from key and value, then
        add to cache if object does not exist in cache.

        :param key: an immutable key
        :param value: an arbitrarily typed value
        :return: None
        """
        from codes.cache_entry import HeapCacheEntry
        cache_entry = HeapCacheEntry(key, value)

        old_cache_entry = self.get_from_lookup_dict(key)
        if old_cache_entry is not None:
            old_cache_entry.value = value
            return
        if self.current_size == self.capacity:
            min_cache_entry = self.data_structure.pop()
            self.pop_from_lookup_dict(min_cache_entry.key)
            self.current_size -= 1
        self.data_structure.push(cache_entry)
        self.add_to_lookup_dict(key, cache_entry)
        self.current_size += 1

    def get(self, key):
        """
        Returns the HeapCacheEntry through O(1) lookup.
        Returns None if key not in cache.

        :param key: an immutable key
        :return: a HeapCacheEntry object or None
        """
        return self.get_from_lookup_dict(key)

    def __repr__(self):
        return "SFCache(" \
               + ','.join([str(cache_ent)
                           for cache_ent in self.data_structure]) \
               + ')'
