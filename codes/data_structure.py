class DLLDataStructure(object):
    def __init__(self):
        from codes.cache_entry import DLLCacheEntry
        self.head = DLLCacheEntry(None, "head")
        self.tail = DLLCacheEntry(None, "tail")
        self.head.next = self.tail
        self.tail.prev = self.head

    def dll_add(self, cache_entry, predecessor):
        """
        Add to the double linked list after DLLCacheEntry="predecessor"

        :param cache_entry: a DLLCacheEntry object
        :param predecessor: DLLCacheEntry object after which to insert cache_entry
        :return: None
        """
        cache_entry.next = predecessor.next
        cache_entry.prev = predecessor
        predecessor.next.prev = cache_entry
        predecessor.next = cache_entry

    def __iter__(self):
        current = self.head.next
        while current != self.tail:
            yield current
            current = current.next


class MinHeapDataStructure(object):
    """
    Supports basic heap operations such as push, pop and peak.
    """

    def __init__(self):
        self.min_heap = []

    def push(self, cache_entry):
        from heapq import heappush
        heappush(self.min_heap, cache_entry)

    def pop(self):
        from heapq import heappop
        return heappop(self.min_heap)

    def peak(self):
        return self.min_heap[0]

    def __iter__(self):
        return iter(self.min_heap)
