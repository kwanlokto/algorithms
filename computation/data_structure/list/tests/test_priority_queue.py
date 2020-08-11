import unittest

from computation.data_structure.list.priority_queue import PriorityQueue


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityQueue()

    def test_push(self):
        self.pq.push(2)
        assert str(self.pq) == "[2]"
        self.pq.push(10)
        assert str(self.pq) == "[10, 2]"
        self.pq.push(3)
        assert str(self.pq) == "[10, 3, 2]"
        self.pq.push(20)
        assert str(self.pq) == "[20, 10, 3, 2]"

    def test_remove(self):
        self.pq.push(10)
        self.pq.push(2)
        self.pq.push(3)

        result = self.pq.pop()

        assert result == 10
        assert str(self.pq) == "[3, 2]"

    def test_build_pq(self):
        arr = [12, 24, 1, 2, 3, 12, 2]
        pq = PriorityQueue.build_priority_queue(arr)

        assert str(pq) == "[24, 12, 12, 2, 3, 1, 2]"
