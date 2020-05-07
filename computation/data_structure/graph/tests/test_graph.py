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

    def test_dijkstra(self):
        graph = Graph(
            [
                [0, 4, 0, 0, 0, 0, 0, 8, 0],
                [4, 0, 8, 0, 0, 0, 0, 11, 0],
                [0, 8, 0, 7, 0, 4, 0, 0, 2],
                [0, 0, 7, 0, 9, 14, 0, 0, 0],
                [0, 0, 0, 9, 0, 10, 0, 0, 0],
                [0, 0, 4, 14, 10, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 2, 0, 1, 6],
                [8, 11, 0, 0, 0, 0, 1, 0, 7],
                [0, 0, 2, 0, 0, 0, 6, 7, 0],
            ],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
        )
        shortest_paths = graph.dijkstra(0)
        self.assertDictEqual(
            shortest_paths,
            {0: 0, 1: 4, 2: 12, 3: 19, 4: 21, 5: 11, 6: 9, 7: 8, 8: 14},
        )
