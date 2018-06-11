from codes.eviction_strategy import LRUEvictionStrategy, MRUEvictionStrategy, SmallestFirstEvictionStrategy

# Smallest First has been implemented as a custom strategy.

EVICTION_STRATEGY_REGISTRY = {
    "LRU": LRUEvictionStrategy,
    "MRU": MRUEvictionStrategy,
    "SF": SmallestFirstEvictionStrategy
}


def eviction_factory(eviction_strategy):
    if eviction_strategy not in EVICTION_STRATEGY_REGISTRY:
        raise ValueError('{} is not an expected eviction strategy'.format(eviction_strategy))

    return EVICTION_STRATEGY_REGISTRY[eviction_strategy]