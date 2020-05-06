import numpy as np


class Graph:
    def __init__(self, adjacency_matrix: list, nodes: list):
        self.nodes = nodes
        self.adjacency_matrix = adjacency_matrix
        if len(nodes) != len(adjacency_matrix):
            raise Exception("Mismatch in the number of nodes")

    def bfs(self, start_node, fcn=None, **kwargs):
        """
        Breadth first search

        Args:
            start_node (int): index in self.adjacency_matrix
            fcn (function): Function to run on each node
        """
        matrix = np.array(self.adjacency_matrix)
        visited = []
        queue = [start_node]
        while len(queue) > 0:
            node = queue.pop(0)

            if node not in visited:
                if fcn is not None:
                    fcn(self.nodes, node, **kwargs)
                visited.append(node)
                for child in np.where(matrix[node] == 1)[0]:
                    queue.append(child)

    def dfs(self, start_node, fcn=None, **kwargs):
        """
        Depth first search.

        Args:
            start_node (int): index in self.adjacency_matrix
            fcn (function): Function to run on each node
        """
        matrix = np.array(self.adjacency_matrix)
        visited = []
        queue = [start_node]
        while len(queue) > 0:
            node = queue.pop(-1)

            if node not in visited:
                if fcn is not None:
                    fcn(self.nodes, node, **kwargs)
                visited.append(node)
                for child in np.where(matrix[node] == 1)[0]:
                    queue.append(child)
