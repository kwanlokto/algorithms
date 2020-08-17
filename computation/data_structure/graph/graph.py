import numpy as np


class Graph:
    def __init__(self, adjacency_matrix: list, values: list):
        if len(values) != len(adjacency_matrix):
            raise Exception("Mismatch in the number of nodes")
        self.values = values
        self.adjacency_matrix = adjacency_matrix
        self.num_nodes = len(values)

    def bfs(self, start_node, fcn=None, parent=None, **kwargs):
        """
        Breadth first search

        Args:
            start_node (int): index in self.adjacency_matrix
            fcn (function): Function to run on each node
            parent (list): Parents of each node
        """
        matrix = np.array(self.adjacency_matrix)
        visited = []
        queue = [start_node]
        while len(queue) > 0:
            node = queue.pop(0)
            if fcn is not None:
                fcn(self.values, node, **kwargs)

            for child in np.where(matrix[node] > 0)[0]:
                if child not in visited:
                    queue.append(child)
                    visited.append(child)
                    if parent is not None:
                        parent[child] = node

    def dfs(self, start_node, fcn=None, parent=None, **kwargs):
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
                    fcn(self.values, node, **kwargs)
                visited.append(node)
                for child in np.where(matrix[node] != 0)[0]:
                    queue.append(child)

    def dijkstra(self, start_node):
        """
        Dijkstra's shortest path algorithm

        Args:
            start_node (int): starting node
        Returns:
            dict: distance from start node to every other node
        """
        explored_nodes = set([start_node])
        matrix = np.array(self.adjacency_matrix)
        distance = {
            node: np.inf if node != start_node else 0
            for node in range(self.num_nodes)
        }
        while len(explored_nodes) != self.num_nodes:
            min_dist = np.inf
            visited_node = None
            for node in distance:
                for child in np.where(matrix[node] != 0)[0]:
                    dist = distance[node] + matrix[node][child]
                    if child not in explored_nodes and dist < min_dist:
                        min_dist = dist
                        visited_node = child
            distance[visited_node] = min_dist
            explored_nodes.add(visited_node)

        return distance
