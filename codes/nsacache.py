from codes.cache import Cache


class NSACache(object):
    """
    An implementation of an n-way set associative cache.

    Performs O(1) lookups against elements in each cache.
    Key and value types have to match key_type and value_type specified at instantiation.
    """

    def __init__(self, eviction_strategy, num_caches,
                 cache_size, key_type,
                 value_type):
        """
        Smallest First strategy implemented as custom strategy.

        :param eviction_strategy: One of ["LRU", "MRU", "SF"] by default.
        :param num_caches: Number of caches.
        :param cache_size: Size of each cache.
        :param key_type: Type of keys. Once chosen, every key has to be of this type.
        :param value_type: Type of values. Once chose, every value has to be of this type.
        """
        self.eviction_strategy = eviction_strategy
        self.num_caches = num_caches
        self.cache_size = cache_size

        self.check_key_type_immutable(key_type)
        self.key_type = key_type
        self.value_type = value_type

        self.caches = [Cache(eviction_strategy, cache_size) for _ in range(num_caches)]

    def get(self, key, fallback=None):
        """
        Get value associated with key if key exists in cache. (Amortized O(1) lookup)
        Raises KeyError if key not in cache.

        :param key: A key of "key_type" specified at instantiation
        :param fallback: Arbitrary fallback value to return in case key does not exist in cache.
        :return: value of type "value_type" specified at instantiation or fallback value
        """

        cache = self.caches[self.get_cache_from_key(key)]
        result = cache.get(key)
        if result is None:
            if fallback is not None:
                return fallback
            else:
                raise KeyError('Key {} not found.'.format(key))
        return result

    def put(self, key, value):
        """
        Put key value into one of the "num_cache" caches.
        Key and value types have to match key_type and value_type specified at instantiation.

        :param key: Key of type "key_type" specified at instantiation
        :param value: Value of type "value_type" specified at instantiation
        :return: None
        """

        self._validate_kv_type(key, value)

        cache = self.caches[self.get_cache_from_key(key)]
        cache.put(key, value)

    def get_cache_from_key(self, key):
        """
        Chose cache (one of num_cache caches) that shall be deterministically be associated with a key.

        :param key: key of type "key_type" specified at instantiation
        :return: Index of cache that shall be associated with a key
        """
        return abs(hash(key)) % self.num_caches

    def _validate_kv_type(self, key, value):
        """
        Validate whether the key and value passed to the put() method are of the type specified at instantiation.
        Raise ValuError if condition not satisfied.

        :param key: Key of type "key_type" specified at instantiation
        :param value: Value of type "value_type" specified at instantiation
        :return: None
        """
        if not isinstance(key, self.key_type):
            raise TypeError('Key is of type {}. '
                            '{} expected. '.format(type(key), self.key_type))
        if not isinstance(value, self.value_type):
            raise TypeError('Value is of type {}. '
                            '{} expected. '.format(type(value), self.value_type))

    @staticmethod
    def check_key_type_immutable(key_type):
        """
        You can only have keys of types which are immutable.

        :param key_type: Key of type "key_type" specified at instantiation
        :return: None
        """

        allowed_types = [int, float, complex,
                         bool, str, tuple,
                         range, frozenset, bytes]
        if key_type not in allowed_types:
            raise ValueError('key type cannot be mutable ({} provided). '
                             'Provide different key_type'.format(key_type))
