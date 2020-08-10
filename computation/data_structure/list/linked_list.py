class LinkedList:
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None

    def insert(self, item, idx=None):
        """
        Insert an item at the desired index. If idx is None, then
        append the item the end of the list

        Args:
            item (Object): Item to insert
            idx (int): index to insert item at (> 0)
        """
        if idx == 0:
            curr_node = LinkedList(self.item)  # Represents self
            # Create a connection for curr_node <-> self.next
            if curr_node.next is not None:
                curr_node.next = self.next
                self.next.prev = curr_node
            # Create a connection for self <-> curr_node
            self.next = curr_node
            curr_node.prev = self

            self.item = item
        else:
            curr = self
            while curr.next is not None and (idx is None or idx > 1):
                if idx is not None:
                    idx -= 1
                curr = curr.next

            if idx is not None and idx > 1:
                raise IndexError(f"list index {idx} out of range")
            next_ = curr.next

            new_node = LinkedList(item)
            # create connection for curr <-> new_node
            new_node.prev = curr
            curr.next = new_node
            # create connection for new_node <-> next_
            if next_ is not None:
                next_.prev = new_node
                new_node.next = next_

    def delete(self, idx):
        """
        Delete the item at the idx-th index from the list

        Args:
            idx (int): index to remove
        """
        # Count to the end or to the index
        if idx == 0:
            if self.next is not None:
                self.item = self.next.item
                self.next = self.next.next
                self.next.prev = self
            else:
                raise Exception(
                    f"Linked list must have at least one element"
                )
        else:
            curr = self
            while curr.next is not None and idx > 1:
                idx -= 1
                curr = curr.next

            if idx > 1 or curr.next is None:
                raise IndexError(f"list index {idx} out of range")

            curr.next = curr.next.next

            if curr.next is not None:
                curr.next.prev = curr

    def get_next(self):
        return self.next

    def get_prev(self):
        return self.prev

    def __str__(self):
        return (
            f"{self.item} <-> {self.next}"
            if self.next is not None
            else f"{self.item}"
        )
