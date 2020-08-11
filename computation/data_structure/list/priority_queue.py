class PriorityQueue:
    """
    Construct a Priority Queue from a max heap using a list implementation
    (logic is the same as binary tree implementation)
    """

    def __init__(self):
        self._items = []

    @classmethod
    def build_priority_queue(cls, arr):
        """
        Construct a priority queue from an array

        Args:
            arr (list): list of items we want to max heapify
        """
        new_heap = cls()
        new_heap._items = arr
        for i in range(int(len(arr) / 2), -1, -1):
            new_heap.max_heapify(i)
        return new_heap

    def push(self, item):
        self._items.insert(0, item)
        self.max_heapify(0)

    def pop(self):
        """
        Retrieve the item with the highest priority (should be
        the first element in self._items)
        """
        last_element = self._items.pop(-1)
        first_element = self._items[0]
        self._items[0] = last_element
        self.max_heapify(0)

        return first_element

    def max_heapify(self, curr_node):
        """
        Reformat self._items such that the list follows max heap
        properties:
            - for any given node C, if P is a parent node of C,
              then the key (the value) of P is greater than or
              equal to the key of C

        Args:
            curr_node (int): index of the current node
        """
        left = 2 * curr_node + 1
        right = 2 * curr_node + 2

        largest = curr_node  # Case where current node is the largest
        if (
            left < len(self._items)
            and self._items[left] > self._items[largest]
        ):
            largest = left
        if (
            right < len(self._items)
            and self._items[right] > self._items[largest]
        ):
            largest = right

        # Swap current node with largest node and ensure that
        # max heap property is satisfied in subgraph
        if largest != curr_node:
            temp = self._items[curr_node]
            self._items[curr_node] = self._items[largest]
            self._items[largest] = temp

            self.max_heapify(largest)

    def __str__(self):
        return f"{self._items}"


class PriorityElement:
    def __init__(self, value, priority):
        self.value = value
        self.priority = priority

    # Note that in Python 2.5 and onwards, the class must define
    # __eq__(), but only one of __lt__(), __le__(), __gt__(), or
    # __ge__() is needed in addition to that
    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority
