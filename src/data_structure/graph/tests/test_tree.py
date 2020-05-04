import unittest

from src.data_structure.graph.tree import Tree


class TestTree(unittest.TestCase):
    def setUp(self):
        # Proper adjacency matrix
        nodes = [1, 2, 3]
        adj_matrix = [[0, 0, 1], [1, 0, 1], [0, 0, 0]]
        self.tree = Tree(adj_matrix, nodes)

    def test_topological_sort(self):
        self.assertEqual(self.tree.root_node, 2)

    def test_bad_adj_matrix(self):
        adj_matrix = [
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
        ]  # adj matrix with a cycle
        with self.assertRaises(Exception) as context:
            Tree(adj_matrix, [1, 2, 3])

        self.assertTrue(
            "Graph provided has a cycle" in str(context.exception)
        )
