import unittest

from computation.data_structure.graph.graph import Graph


class TestTree(unittest.TestCase):
    def setUp(self):
        # Proper adjacency matrix
        nodes = [1, 2, 3, 4]
        adj_matrix = [
            [0, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 1, 0, 0],
        ]
        self.graph = Graph(adj_matrix, nodes)

    def test_bfs(self):
        order = []

        def fcn(nodes, node_idx, visited):
            visited.append(node_idx)

        self.graph.bfs(0, fcn, visited=order)
        self.assertListEqual(order, [0, 1, 2, 3])

    def test_dfs(self):
        order = []

        def fcn(nodes, node_idx, visited):
            visited.append(node_idx)

        self.graph.dfs(0, fcn, visited=order)
        self.assertListEqual(order, [0, 3, 1, 2])
