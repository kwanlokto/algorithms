import unittest

from computation.data_structure.graph.tree import Tree


class TestTree(unittest.TestCase):
    def setUp(self):
        # Proper adjacency matrix
        nodes = [1, 2, 3]
        adj_matrix = [[0, 0, 1], [1, 0, 0], [0, 0, 0]]
        self.tree = Tree(adj_matrix, nodes)

    def test_topological_sort(self):
        self.assertEqual(self.tree.root_node, 1)

    def test_cycle(self):
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

    def test_unique_parent(self):
        adj_matrix = [
            [0, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]  # disconnected tree and more than one path to parent
        with self.assertRaises(Exception) as context:
            Tree(adj_matrix, [1, 2, 3, 4])

        self.assertTrue(
            "More than one path from root to nodes: [2]."
            in str(context.exception)
        )
        self.assertTrue("Tree is not connected." in str(context.exception))

    def test_get_depth(self):
        depth = self.tree.get_depth(2)
        self.assertEqual(depth, 2)

    def test_construct_graph_of_nodes(self):
        root_node = self.tree.construct_graph_of_nodes()

        assert str(root_node) == "2 -> 1 -> 3"
