from codes.eviction_factory import eviction_factory


class Cache(object):
    """
    A cache responsible for:
    1. Passing on put() and get() methods to an eviction_strategy
        implementation through a chain of responsibility.
    2. Providing O(1) lookup functionality for the eviction strategy
        implementation.

    What the cache is not responsible for:
    1. Defining and maintaining the data structure for an eviction strategy's
        idiosyncratic requirements.
    2. Not responsible for defining which object to evict.

    To wire in a "Custom" strategy, remember to:
    1. Write custom implementation inside eviction_strategy.py
    2. Add it to the EVICTION_STRATEGY_REGISTRY (inside eviction_factory.py)

    """

    def __init__(self, eviction_strategy, capacity):
        """
        :param eviction_strategy: One of ["LRU", "MRU", "SF"] by default.
        :param capacity: Size of the cache.
        """

        self.eviction_strategy = eviction_factory(eviction_strategy)()
        self.capacity = capacity
        self.current_size = 0
        self.lookup_dict = {}

    def put(self, key, value):
        """
        Insert the key-value pair object into cache.

        :param key: Key of type "key_type" specified at instantiation of
        NSACache
        :param value: Value of type "value_type" specified at instantiation of
        NSACache
        :return: None
        """
        if key is None:
            raise ValueError('Key cannot be None')
        self.eviction_strategy.put(self, key, value)

    def get(self, key):
        """
        Get the key-value pair object from the cache. Amortized O(1) lookup.

        :param key: Key of type "key_type" specified at instantiation of
        NSACache.
        :return: Value of type "value_type" specified at instantiation of
        NSACache.
        """

        result = self.eviction_strategy.get(self, key)
        if result is not None:
            return result.value
        return None

    def exists_in_lookup_dict(self, item):
        return item.key in self.lookup_dict

    def get_from_lookup_dict(self, key):
        """
        Amortized O(1) lookup for a key in this cache's dictionary.

        :param key: Key of type "key_type" specified at instantiation of
        NSACache.
        :return: Value of type "value_type" specified at instantiation of
        NSACache.
        """
        return self.lookup_dict.get(key, None)

    def pop_from_lookup_dict(self, key):
        """
        Remove a key-value pair only from the cache's dictionary.

        :param key: Key of type "key_type" specified at instantiation of
        NSACache.
        :return: Key-value pair object that this key shall map to.
        """
        return self.lookup_dict.pop(key)

    def add_to_lookup_dict(self, key, to_add):
        """
        Add a key-value pair to this cache's dictionary for fast lookup.

        :param key: Key of type "key_type" specified at instantiation of
        NSACache
        :param to_add: Key-value pair object that this key shall map to.
        :return: None
        """
        self.lookup_dict[key] = to_add
