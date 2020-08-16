import unittest
from unittest.mock import patch

from computation.data_structure.graph.AVL_tree import (
    AVLTree,
    balance_tree,
    check_balance_factors,
    get_children_height,
    get_inorder_successor,
    left_rotation,
    right_rotation,
    update_height_bottom_up,
)


class TestAVLTree(unittest.TestCase):
    def setUp(self):
        # Add connections
        self.parent = AVLTree(11)
        self.root_node = AVLTree(10, self.parent)
        self.parent.left = self.root_node
        self.left_node = AVLTree(8, self.root_node)
        self.root_node.left = self.left_node
        self.l_leaf_node = AVLTree(7, self.left_node)
        self.left_node.left = self.l_leaf_node
        self.r_leaf_node = AVLTree(9, self.left_node)
        self.left_node.right = self.r_leaf_node

        # Assign correct heighs
        self.parent.height = 3
        self.root_node.height = 2
        self.left_node.height = 1

    def test_string_representation(self):
        assert (
            str(self.parent) == "11 -> [10 -> [8 -> [7, 9], None], None]"
        )

    def test_insert(self):
        root = AVLTree(5)
        root.insert(4)
        root.insert(3)
        root.insert(2)
        root.insert(1)
        assert str(root) == "4 -> [2 -> [1, 3], 5]"

    def test_delete(self):
        root = AVLTree(5)
        root.insert(6)
        root.insert(3)
        root.insert(2)

        root.delete(6)
        assert str(root) == "3 -> [2, 5]"

        root.delete(3)
        assert str(root) == "2 -> [None, 5]"

        root.delete(2)
        assert str(root) == "5"

    def test_insert_delete(self):
        root = AVLTree(5)
        root.insert(6)
        root.insert(3)
        root.insert(2)
        root.delete(3)

        root.insert(3)
        assert str(root) == "5 -> [2 -> [None, 3], 6]"

        root.delete(5)
        assert str(root) == "3 -> [2, 6]"

    @patch("computation.data_structure.graph.AVL_tree.balance_tree")
    def test_right_rotation(self, mock_balance_tree):
        mock_balance_tree.return_value = None
        right_rotation(self.root_node)

        new_root = self.parent.left
        assert new_root.value == 8
        assert new_root.left.value == 7
        assert new_root.right.value == 10
        assert new_root.right.left.value == 9
        assert new_root.right.right is None

    @patch("computation.data_structure.graph.AVL_tree.balance_tree")
    def test_left_rotation(self, mock_balance_tree):
        mock_balance_tree.return_value = None
        parent = AVLTree(11)
        root_node = AVLTree(7, parent)
        parent.left = root_node
        right_node = AVLTree(9, root_node)
        root_node.right = right_node

        l_leaf_node = AVLTree(8, right_node)
        right_node.left = l_leaf_node
        r_leaf_node = AVLTree(10, right_node)
        right_node.right = r_leaf_node

        left_rotation(root_node)

        new_root = parent.left

        assert new_root.value == 9
        assert new_root.right.value == 10
        assert new_root.left.value == 7
        assert new_root.left.right.value == 8
        assert new_root.left.left is None

    def test_get_inorder_successor(self):
        result = get_inorder_successor(self.root_node)

        assert result == self.r_leaf_node

    def test_get_inorder_successor_none(self):
        result = get_inorder_successor(AVLTree(10))

        assert result is None

    def test_check_balance_factors(self):
        result = check_balance_factors(self.l_leaf_node)
        assert result == self.root_node

        result = check_balance_factors(self.r_leaf_node)
        assert result == self.root_node

    def test_check_balance_factors_balanced(self):
        parent = AVLTree(11)
        root_node = AVLTree(7, parent)
        result = check_balance_factors(root_node)
        assert result is None

    def test_update_height_bottom_up(self):
        self.parent.height = 0
        self.root_node.height = 0
        self.left_node.height = 0

        update_height_bottom_up(self.l_leaf_node)

        assert self.parent.height == 3
        assert self.root_node.height == 2
        assert self.left_node.height == 1

    def test_get_children_height(self):
        left, right = get_children_height(self.root_node)
        assert left == 1
        assert right == -1

    @patch(
        "computation.data_structure.graph.AVL_tree.update_height_bottom_up"
    )
    @patch(
        "computation.data_structure.graph.AVL_tree.check_balance_factors"
    )
    @patch("computation.data_structure.graph.AVL_tree.get_children_height")
    @patch("computation.data_structure.graph.AVL_tree.right_rotation")
    def test_balance_tree(
        self,
        mock_right_rotation,
        mock_get_children_height,
        mock_check_balance_factors,
        mock_update_height_bottom_up,
    ):
        mock_check_balance_factors.return_value = self.root_node
        mock_get_children_height.return_value = (2, 0)

        balance_tree(self.l_leaf_node)

        assert mock_check_balance_factors.call_count == 1
        assert mock_update_height_bottom_up.call_count == 1
        assert mock_get_children_height.call_count == 1
        assert mock_right_rotation.call_count == 1
