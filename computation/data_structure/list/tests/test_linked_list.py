import unittest

from computation.data_structure.list.linked_list import LinkedList


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.linked_list = LinkedList(0)

    def test_print(self):
        self.linked_list.next = LinkedList(1)
        assert str(self.linked_list) == "0 <-> 1"

    def test_insert(self):
        self.linked_list.insert(1, 0)
        assert str(self.linked_list) == "1 <-> 0"
        assert self.linked_list.next.prev == self.linked_list

        self.linked_list.insert(10)
        assert str(self.linked_list) == "1 <-> 0 <-> 10"
        assert self.linked_list.next.next.prev == self.linked_list.next

    def test_delete(self):
        for i in range(1, 4):
            self.linked_list.insert(i)
        self.linked_list.delete(0)

        assert str(self.linked_list) == "1 <-> 2 <-> 3"

        self.linked_list.delete(1)
        assert str(self.linked_list) == "1 <-> 3"

        self.linked_list.delete(1)
        assert str(self.linked_list) == "1"

    def test_get_next(self):
        self.linked_list.insert(1)
        assert self.linked_list.next == self.linked_list.get_next()

    def test_get_previous(self):
        self.linked_list.insert(1)
        next_ = self.linked_list.get_next()
        assert next_.get_prev() == self.linked_list
