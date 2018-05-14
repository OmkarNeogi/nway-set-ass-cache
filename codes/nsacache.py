class NSACache(object):
    def __init__(self, key_type,
                 val_type, eviction_strategy,
                 num_cache, cache_size, hashing_function=None):
        self.key_type = key_type
        self.val_type = val_type
        self.check_key_type_immutable(key_type)

        self.eviction_strategy = eviction_strategy
        self.num_cache = num_cache
        self.cache_size = cache_size
        self.hash_func = hashing_function

        self.caches = self.get_n_caches(eviction_strategy,
                                        num_cache,
                                        cache_size)

    def put(self, key, value):
        self._validate_kv_type(key, value)
        cache = self.caches[self._hash_key_to_cache(key)]
        cache.put(key, value)

    def get(self, key, fallback=None):
        cache = self.caches[self._hash_key_to_cache(key)]
        response = cache.get(key)
        if response is None:
            if fallback is not None:
                return fallback
            raise KeyError('Key {} not found.'.format(key))
        return response

    @staticmethod
    def check_key_type_immutable(key_type):
        allowed_types = [int, float, complex,
                         bool, str, tuple,
                         range, frozenset, bytes]
        if key_type not in allowed_types:
            raise ValueError('key type cannot be mutable ({} provided). '
                             'Provide different key_type'.format(key_type))

    def _validate_kv_type(self, key, value):
        if not isinstance(key, self.key_type):
            raise TypeError('Key is of type {}. '
                            '{} expected. '.format(type(key), self.key_type))
        if not isinstance(value, self.val_type):
            raise TypeError('Value is of type {}. '
                            '{} expected. '.format(type(value), self.val_type))

    def _hash_key_to_cache(self, key):
        if self.hash_func is not None:
            # user defined hashing function for better availability
            cache_index = self.hash_func(key, self.num_cache)
            return cache_index
        else:
            return abs(hash(key)) % self.num_cache

    @staticmethod
    def get_n_caches(eviction_strategy, num_cache, cache_size):

        if eviction_strategy == "LRU":
            from codes.cache import LRUCache
            return [LRUCache(cache_size) for _ in range(num_cache)]
        elif eviction_strategy == "MRU":
            from codes.cache import MRUCache
            return [MRUCache(cache_size) for _ in range(num_cache)]
        elif eviction_strategy in ["SF", "Smallest"]:
            from codes.cache import SFCache
            return [SFCache(cache_size) for _ in range(num_cache)]

        raise ValueError('{} is not an accepted eviction strategy'
                         .format(eviction_strategy))


if __name__ == "__main__":
    nsac = NSACache(int, int, "SF", 1, 3)
    nsac.put("2", 1)
    nsac.put(2, 2)
    nsac.put(3, 3)
    nsac.put(4, 4)
    x = nsac.get(2)
    nsac.put(5, 5)
    nsac.put(4, 4)
    nsac.put(6, 6)
    n = nsac.get(10, 5)
    print(nsac.caches[0])
