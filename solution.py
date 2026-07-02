import heapq
from typing import Optional


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev: Optional["_Node"] = None
        self.next: Optional["_Node"] = None


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.map = {}
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _push_front(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._remove(node)
            self._push_front(node)
            return
        if len(self.map) >= self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        node = _Node(key, value)
        self.map[key] = node
        self._push_front(node)


def can_attend_all(events):
    if not events:
        return True
    events = sorted(events)
    for i in range(1, len(events)):
        if events[i][0] < events[i - 1][1]:
            return False
    return True


def min_rooms_required(events):
    if not events:
        return 0
    events = sorted(events)
    heap = []
    rooms = 0
    for start, end in events:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
        rooms = max(rooms, len(heap))
    return rooms


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    print(cache.get(1))      # 1
    cache.put(3, 3)          # evicts key 2
    print(cache.get(2))      # -1
    cache.put(4, 4)          # evicts key 1
    print(cache.get(1))      # -1
    print(cache.get(3))      # 3
    print(cache.get(4))      # 4

    print(can_attend_all([(9, 10), (10, 11), (11, 12)]))   # True
    print(can_attend_all([(9, 12), (10, 11)]))             # False
    print(min_rooms_required([(9, 10), (10, 11)]))         # 1
    print(min_rooms_required([(0, 30), (5, 10), (15, 20)]))  # 2
