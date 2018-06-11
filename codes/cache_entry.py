class CacheEntry(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return "CacheEntry(" + str(self.key) + "," + str(self.value) + ")"

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        return self.key < other.key


class DLLCacheEntry(CacheEntry):
    def __init__(self, key, value):
        super().__init__(key, value)

        self.next = None
        self.prev = None

    def disconnect(self):
        self.next.prev = self.prev
        self.prev.next = self.next
