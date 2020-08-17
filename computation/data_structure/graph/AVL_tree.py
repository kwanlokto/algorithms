from computation.data_structure.graph.node import Node


class AVLTree(Node):
    """
    Self-balancing binary tree
    """

    def __init__(self, value, parent=None):
        super().__init__(value)
        self.parent = parent  # If parent is None then self is root
        self.left = None
        self.right = None
        self.height = 0

    # Super function should not be called
    def add_child(self, value):
        raise Exception("Function is not defined for AVL tree")

    def insert(self, value):
        """
        Add new item to the bottom of the AVL tree, then rebalance
        the tree

        Args:
            value: value to insert into the tree
        """
        new_node = self.__insert_to_bottom(value)
        balance_tree(new_node)

    def delete(self, value):
        """
        Delete an item from the AVL tree then rebalance the tree

        Args:
            value: value to remove from the tree
        """

        def replace_with_node(node_to_replace, replacement_node):
            if replacement_node is not None:
                node_to_replace.value = replacement_node.value
            else:
                if node_to_replace.parent is None:
                    raise Exception("AVL cannot be empty")
                if node_to_replace.parent.left == node_to_replace:
                    node_to_replace.parent.left = None
                elif node_to_replace.parent.right == node_to_replace:
                    node_to_replace.parent.right = None

        node_to_remove = self.__find_node_in_tree(value)
        if node_to_remove is None:
            raise Exception("{value} is not found in AVL tree")

        tree_to_balance = node_to_remove.parent
        if node_to_remove.left is None and node_to_remove.right is None:
            replace_with_node(node_to_remove, None)
        # node to delete has a right child
        elif node_to_remove.left is None:
            replace_with_node(node_to_remove, node_to_remove.right)
            node_to_remove.right = None
        # node to delete has a left child
        elif node_to_remove.right is None:
            replace_with_node(
                node_to_remove, node_to_remove.left,
            )
            node_to_remove.left = None
        else:
            successor = get_inorder_successor(node_to_remove)
            node_to_remove.value = successor.value
            replace_with_node(successor, None)

            tree_to_balance = successor.parent
        balance_tree(tree_to_balance)

    def __find_node_in_tree(self, value):
        """
        Search for a node in the tree

        Args:
            value: value to look for in the tree
        Returns:
            AVLTree: node that has value 'value'
        """
        queue = [self]
        while len(queue):
            node = queue.pop(0)
            if node.value == value:
                return node
            elif node.value > value and node.left is not None:
                queue.append(node.left)
            elif node.value <= value and node.right is not None:
                queue.append(node.right)
        return None

    def __insert_to_bottom(self, value):
        """
        BFS to put value at the first node that does not have a
        branching factor of 2

        Args:
            value: value to insert into the tree
        Returns:
            AVLTree: node that has been added to the tree
        """
        queue = [self]
        while len(queue):
            node = queue.pop(0)
            if node.value > value:
                if node.left is not None:
                    queue.append(node.left)
                else:
                    node.left = AVLTree(value, parent=node)
                    return node.left

            elif node.value <= value:
                if node.right is not None:
                    queue.append(node.right)
                else:
                    node.right = AVLTree(value, parent=node)
                    return node.right
        return None

    def __str__(self):
        str_node = f"{self.value}"
        if self.left is not None or self.right is not None:
            str_node += f" -> [{self.left}, {self.right}]"
        return str_node

    def __repr__(self):
        return f"AVLTree({self.value})"

    def __lt__(self, other):
        return isinstance(other, AVLTree) and self.value < other.value

    def __eq__(self, other):
        return isinstance(other, AVLTree) and self.value == other.value


def balance_tree(node):
    """
    Update the heights from the root to node and check if the
    subtree is balanced at node. If not balance the subtree
    by performing several rotations on the subgraph

    Args:
        node (Node): subtree we want to check if it is balanced
    """
    update_height_bottom_up(node)
    unbalance_subtree = check_balance_factors(node)

    if unbalance_subtree is not None:
        left, right = get_children_height(unbalance_subtree)
        if left > right:  # Right rotation
            right_rotation(unbalance_subtree)

        elif right > left:  # Left rotation
            left_rotation(unbalance_subtree)


def get_children_height(node):
    """
    Get the height of node's left child and right child. If a child
    does not exist the height returned is -1

    Args:
        node (Node): parent of nodes whose height we want to retrieve
    Returns:
        tuple: left subtree's height and right subtree's height
    """
    left = -1 if node.left is None else node.left.height
    right = -1 if node.right is None else node.right.height
    return left, right


def update_height_bottom_up(node):
    """
    Update the height starting at 'node' and stopping when we reach the
    root of the tree

    Args:
        node (Node): starting node
    """
    curr_node = node
    while curr_node is not None:
        left, right = get_children_height(curr_node)
        curr_node.height = max(left, right) + 1
        curr_node = curr_node.parent


def check_balance_factors(node):
    """
    Check the balance factors of the left and right subtree from 'node'
    to the root

    Args:
        node (Node): starting node
    Returns:
        Node: first occurring node that has a balance factor > 1
                (root of unbalanced subtree)
    """
    curr_node = node
    while curr_node is not None:
        left, right = get_children_height(curr_node)
        if abs(left - right) > 1:
            return curr_node
        curr_node = curr_node.parent
    return None


def left_rotation(node):
    # move right child over to the left side of node
    old_right = node.right
    old_left = node.left

    node.right = old_right.right
    if old_right.right is not None:
        old_right.right.parent = node
    node.left = old_right
    old_right.right = old_right.left
    old_right.left = old_left
    if old_left is not None:
        old_left.parent = old_right

    # update values
    old_root = node.value
    node.value = old_right.value
    old_right.value = old_root

    balance_tree(old_right)


def right_rotation(node):
    # move left child over to the right side of node
    old_right = node.right
    old_left = node.left

    node.left = old_left.left
    if old_left.left is not None:
        old_left.left.parent = node
    node.right = old_left
    old_left.left = old_left.right
    old_left.right = old_right
    if old_right is not None:
        old_right.parent = old_left

    # update values
    old_root = node.value
    node.value = old_left.value
    old_left.value = old_root

    balance_tree(old_left)


def get_inorder_successor(node):
    """
    Node with a maximum value of a key in the left subtree

    Returns:
        Node: the next successor for node, if there is one in the left
              subtree, otherwise return None
    """
    curr_node = node.left
    if curr_node is None:
        return None
    while curr_node.right is not None:
        curr_node = curr_node.right
    return curr_node
