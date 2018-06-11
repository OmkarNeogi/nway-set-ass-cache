class CacheEntry(object):
    """
    Generic CacheEntry object for storing key and value in a cache.
    """

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
    """
    a CacheEntry object specialised for DoubleLinkedLists.
    """

    def __init__(self, key, value):
        super().__init__(key, value)

        self.next = None
        self.prev = None

    def disconnect(self):
        """
        Disconnect a LinkedList node by wiring the node previous and next to
        the current node.

        :return: None
        """
        self.next.prev = self.prev
        self.prev.next = self.next
