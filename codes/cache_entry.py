from abc import ABC


class CacheEntry(ABC):
    def __init__(self, key, val):
        self.key = key
        self.val = val

    def __repr__(self):
        # All values are expected have a repr function.
        # For custom objects this will not work
        try:
            return "CacheEntry(" + str(self.key) + "," + str(self.val) + ")"
        except NotImplementedError:
            # Dont know for sure the name of this error when
            # repr for value is not implemented
            return "Implement __repr__ for values of NSACache"

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
        self.prev.next = self.next
        self.next.prev = self.prev


class HeapCacheEntry(CacheEntry):
    def __init__(self, key, val):
        super().__init__(key, val)
