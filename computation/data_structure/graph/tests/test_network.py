import unittest

from computation.data_structure.graph.network import Network


class TestNetwork(unittest.TestCase):
    def setUp(self):
        adj_matrix = [
            [0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ]
        self.network = Network(adj_matrix)

    def test_ford_fulkerson(self):
        max_flow = self.network.ford_fulkerson(0, 5)
        assert max_flow == 23
