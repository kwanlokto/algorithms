import numpy as np

from computation.data_structure.graph.graph import Graph


class Network(Graph):
    def __init__(self, adjacency_matrix):
        super().__init__(adjacency_matrix, [None] * len(adjacency_matrix))

    def ford_fulkerson(self, src, sink):
        """
        Determine the max flow in the network

        Args:
            src (int): Node index of the source
            sink (int): Node index of the sink
        Returns:
            int: Max flow through the network
        """
        # This array is filled by BFS and to store path
        parent = [-1] * (self.num_nodes)

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from src to sink
        visited = []

        def check_connected(nodes, node_idx, visited):
            visited.append(node_idx)

        self.bfs(src, check_connected, parent, visited=visited)

        while sink in visited:
            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = np.inf
            node = sink
            while node != src:
                path_flow = min(
                    path_flow, self.adjacency_matrix[parent[node]][node]
                )
                node = parent[node]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            node = sink
            while node != src:
                self.adjacency_matrix[parent[node]][node] -= path_flow
                self.adjacency_matrix[node][parent[node]] += path_flow
                node = parent[node]

            visited = []
            parent = [-1] * (self.num_nodes)
            self.bfs(src, check_connected, parent, visited=visited)

        return max_flow
