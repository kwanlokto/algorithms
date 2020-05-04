import numpy as np


class Tree:
    def __init__(self, adjacency_matrix: list, nodes: list):
        adjacency_list = {}
        for row_num in range(len(adjacency_matrix)):

            row = adjacency_matrix[row_num]
            adjacency_list[nodes[row_num]] = [
                nodes[col_num]
                for col_num in range(len(row))
                if row[col_num]
            ]
        self.__ordering = topological_sort(adjacency_matrix)
        self.root_node = nodes[self.__ordering[0]]


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
    leaf_nodes = get_empty_columns(matrix)
    sorted_list = []  # list of column numbers
    while len(leaf_nodes) > 0:
        leaf = leaf_nodes.pop(0)
        sorted_list.append(leaf)
        matrix[leaf] = np.zeros(len(matrix))
        leaf_nodes.extend(get_empty_columns(matrix))
    zero_matrix = np.zeros((len(matrix), len(matrix)))

    if not np.array_equal(matrix, zero_matrix):
        raise Exception("Graph provided has a cycle")
    return sorted_list


def __str__(self):
    tree = ""
    return tree
