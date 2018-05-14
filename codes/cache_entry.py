from abc import ABC


class CacheEntry(ABC):
    """
    Abstract class for all CacheEntry objects.
    """

    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __repr__(self):
        # All values are expected have a repr function.
        # For custom objects this will not work
        try:
            _ = str(self.val)
        except NotImplementedError:
            return "Implement __repr__ for values of NSACache"
        # str(self.key) is expected to be of an immutable type
        return "CacheEntry(" + str(self.key) + "," + str(self.val) + ")"

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key


class DLLCacheEntry(CacheEntry):
    def __init__(self, key, val):
        super().__init__(key, val)
        self.prev = None
        self.next = None

    def disconnect(self):
        """
        Remove the connections of this DLLCacheEntry (with the next and
        previous nodes) by joining the next and previous DLLCacheEntry
        nodes to each other.

        :return: None
        """
        self.prev.next = self.next
        self.next.prev = self.prev


class HeapCacheEntry(CacheEntry):
    def __init__(self, key, val):
        super().__init__(key, val)
