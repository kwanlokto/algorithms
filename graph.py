import copy

import numpy as np


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parents = []

    def add_child(self, node):
        if isinstance(node, Node):
            self.children.append(node)

    def add_parent(self, node):
        if isinstance(node, Node):
            self.parents.append(node)


class Tree:
    def __init__(self, adjacency_matrix: np.ndarray, nodes: list):
        adjacency_list = {}
        for row_num in range(len(adjacency_matrix)):

            row = adjacency_matrix[row_num]
            adjacency_list[nodes[row_num]] = [
                nodes[col_num] for col_num in range(len(row)) if row[col_num]
            ]
        ordering = topological_sort(adjacency_matrix)
        self.root_node = nodes[ordering[0]]


def topological_sort(adjacency_matrix: np.ndarray):
    def get_empty_columns(matrix):
        empty = np.zeros(len(matrix)).tolist()

        empty_col_nums = []
        for col_num in range(len(matrix)):
            if matrix[:, col_num] == empty:
                empty_col_nums.append(col_num)
        return empty_col_nums

    matrix = copy.deepcopy(adjacency_matrix)
    root_nodes = get_empty_columns(matrix)
    sorted_list = []  # list of column numbers
    while len(root_nodes) > 0:
        root = root_nodes.pop(0)
        sorted_list.append(root)
        matrix[root] = np.zeros(len(matrix)).tolist()
        root_nodes.extend(get_empty_columns(matrix))
    
    zero_matrix = np.zeros((len(matrix), len(matrix)))
    if np.array_equal(zero_matrix, matrix):
        raise Exception("Graph provided has a cycle")
    return sorted_list
