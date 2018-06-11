class DLLDataStructure(object):
    def __init__(self):
        """
        A data structure for facilitating double linked list style operations and access.
        """

        from codes.cache_entry import DLLCacheEntry

        self.head = DLLCacheEntry(None, "head")
        self.tail = DLLCacheEntry(None, "tail")

        self.head.next = self.tail
        self.tail.prev = self.head

    def __iter__(self):
        current = self.head.next
        while current != self.tail:
            yield current
            current = current.next

    def __repr__(self):
        return ''.join([str(i) for i in self])

    @staticmethod
    def add(cache_entry, predecessor):
        cache_entry.next = predecessor.next
        cache_entry.prev = predecessor

        predecessor.next.prev = cache_entry
        predecessor.next = cache_entry


class HeapDataStructure(object):
    """
    A data structure for facilitating heap style operations and access.
    By default uses a min heap - for the smallest first eviction policy.
    """

    def __init__(self):
        self.min_heap = []

    def __iter__(self):
        return iter(self.min_heap)

    def __repr__(self):
        return ''.join(str(i) for i in self)

    def push(self, cache_entry):
        from heapq import heappush
        heappush(self.min_heap, cache_entry)

    def pop(self):
        from heapq import heappop
        return heappop(self.min_heap)

    def peak(self):
        return self.min_heap[0]
