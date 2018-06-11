from codes.eviction_strategy import LRUEvictionStrategy, MRUEvictionStrategy, \
    SmallestFirstEvictionStrategy

# Smallest First has been implemented as a custom strategy.

"""
This is where you wire in your custom algorithm.
The Smallest first algorithm can serve as an example - it has it's own
(very different from linked list) data structure and different style of
operations (that are done on the data structure - push, peak and pop).
This is why I think it serves as a good example for a custom eviction algorithm
"""

EVICTION_STRATEGY_REGISTRY = {
    "LRU": LRUEvictionStrategy,
    "MRU": MRUEvictionStrategy,
    "SF": SmallestFirstEvictionStrategy
}


def eviction_factory(eviction_strategy):
    """
    Specify the kind of eviction algorithm that shall be used by caches.
    To use a custom algorithm, add it to the dictionary mentioned here
    (inside eviction_factory.py)

    Raises ValueError if the eviction_strategy is not recognised in the
    EVICTION_STRATEGY_REGISTRY.

    :param eviction_strategy: One of the EVICTION_STRATEGY_REGISTRY keys.
    :return:
    """
    if eviction_strategy not in EVICTION_STRATEGY_REGISTRY:
        raise ValueError('{} is not an expected eviction strategy'.format(
            eviction_strategy)
        )

    return EVICTION_STRATEGY_REGISTRY[eviction_strategy]
