import numpy as np

from computation.data_structure.graph.graph import Graph


class Tree(Graph):
    def __init__(self, adjacency_matrix: list, nodes: list):
        super().__init__(adjacency_matrix, nodes)
        self.__ordering = topological_sort(adjacency_matrix)
        self.root_node = self.__ordering[0]
        self.__validate_tree()

    def __str__(self):
        tree = ""
        for node_idx in self.__ordering:
            tree = self.nodes[node_idx]
        return tree

    def get_depth(self, node_idx):
        matrix = np.array(self.adjacency_matrix)
        depth = 0

        while node_idx != self.root_node:
            # Get the node's parent index in the adj matrix
            parent = np.where(matrix[:, node_idx] == 1)[0]
            if len(parent) == 1:
                depth += 1
                node_idx = parent[0]
            else:
                raise Exception(
                    f"Expected to find one parent for {node_idx}"
                )
        return depth

    def __validate_tree(self):
        mult_paths = []
        err_msg = ""
        matrix = np.array(self.adjacency_matrix)
        for node_idx in range(self.num_nodes):
            parent = np.where(matrix[:, node_idx] != 0)[0]
            if len(parent) > 1:  # Check that node has one parent
                mult_paths.append(node_idx)
        if len(mult_paths) > 0:
            err_msg += (
                f"More than one path from root to nodes: {mult_paths}. "
            )

        visited = []

        def check_connected(nodes, node_idx, visited):
            visited.append(node_idx)

        self.bfs(self.root_node, check_connected, visited=visited)
        if len(visited) != self.num_nodes:
            err_msg += "Tree is not connected."

        if err_msg:
            raise Exception(err_msg)


def topological_sort(adjacency_matrix: list):
    found = []  # array to keep track of what has been found

    def get_empty_columns(matrix):
        empty = np.zeros(len(matrix))
        empty_col_nums = []
        for col_num in range(len(matrix)):
            if (
                np.array_equal(matrix[:, col_num], empty)
                and col_num not in found
            ):
                found.append(col_num)
                empty_col_nums.append(col_num)
        return empty_col_nums

    matrix = np.array(adjacency_matrix)
    root_nodes = get_empty_columns(matrix)
    sorted_list = []  # list of column numbers
    while len(root_nodes) > 0:
        leaf = root_nodes.pop(0)
        sorted_list.append(leaf)
        matrix[leaf] = np.zeros(len(matrix))
        root_nodes.extend(get_empty_columns(matrix))
    zero_matrix = np.zeros((len(matrix), len(matrix)))

    if not np.array_equal(matrix, zero_matrix):
        raise Exception("Graph provided has a cycle")
    return sorted_list
