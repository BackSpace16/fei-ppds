import numpy as np
from networkx import DiGraph, single_source_dijkstra_path_length


def adjacency_matrix_to_nxgraph(adj_matrix):
    graph = DiGraph()
    n = len(adj_matrix)

    for i in range(n):
        for j in range(n):
            weight = adj_matrix[i][j]
            if weight != 0 and weight != np.inf:
                graph.add_edge(i, j, weight=weight)

    return graph


def generate_adj_matrix(n_vertices, min_weight, max_weight, edge_density):
    """Generate an adjacency matrix.
    
    Keyword arguments:
    n_vertices -- number of vertices in graph (matrix size)
    min_weight -- minimal value of weights generated
    max_weight -- maximal value of weights generated
    edge_density -- percentage, how dense will be edges in graph
                    (every vertex will have at least one edge)
    """
    adj_matrix = np.random.randint(min_weight, max_weight, size=(n_vertices, n_vertices))
    adj_matrix = adj_matrix.astype(float)
    shape = adj_matrix.shape
    
    total_elements = adj_matrix.size
    zero_count = 100 - int(total_elements * edge_density / 100)
    zero_indices = np.random.choice(total_elements, zero_count, replace=False)

    adj_matrix = adj_matrix.flatten()
    adj_matrix[zero_indices] = 0
    adj_matrix = adj_matrix.reshape(shape)

    adj_matrix[adj_matrix == 0] = np.inf
    np.fill_diagonal(adj_matrix, 0)

    return adj_matrix


def load_adj_matrix(file_path, separator=" ", 
                    skip_rows=0, skip_cols=0, none_edge=0):
    """Load file, and return data as matrix.

    Lines in file should represent rows of an adjacency matrix,
    values should be separated by separator.
    """
    adj_matrix = []

    with open(file_path, 'r', encoding="utf-8") as file:
        for i, line in enumerate(file):
            if i >= skip_rows:
                line = line.strip().split(separator)
                row = line[0+skip_cols:]
                if type(none_edge) == str:
                    row = list(map(lambda x: 0 if x == none_edge else x, row))
                    row = list(map(float, row))
                else:
                    row = list(map(float, row))
                    row = list(map(lambda x: 0 if x == none_edge else x, row))
                adj_matrix.append(row)

    adj_matrix = np.array(adj_matrix, dtype='float32')
    adj_matrix[adj_matrix == 0] = np.inf
    np.fill_diagonal(adj_matrix, 0)

    return adj_matrix


def dijkstra(adj_matrix, vertex_index):
    num_vertices = adj_matrix.shape[0]

    distances = adj_matrix[vertex_index]
    distances[vertex_index] = np.inf

    queue = [i for i in range(0, num_vertices)]
    queue.remove(vertex_index)

    while len(queue):
        u = None
        for i in queue:
            if u != None:
                if distances[i] < distances[u]:
                    u = i
            else:
                u = i

        queue.remove(u)
        for v in range(len(adj_matrix[u])):
            if v in queue and adj_matrix[u][v] != np.inf:
                alt = distances[u] + adj_matrix[u][v]
                if alt < distances[v]:
                    distances[v] = alt

    return distances


def all_dijkstra(adj_matrix):
    """Find shortest path from all to all vertices in graph.

    Keyword arguments:
    adj_matrix -- adjacency matrix of a graph
    """
    distances = []
    for vertex_index in range(len(adj_matrix)):
        row = dijkstra(adj_matrix, vertex_index)
        distances.append(row)

    distances = np.array(distances, dtype='float32')
    return distances


def main():
    adj_matrix = load_adj_matrix("inputs/input2.txt")
    adj_matrix = generate_adj_matrix(10, 1, 20, 100)
    print(adj_matrix)

    distances = all_dijkstra(adj_matrix)
    print(distances)
    
    nxgraph = adjacency_matrix_to_nxgraph(adj_matrix)
    nx_distances = single_source_dijkstra_path_length(nxgraph, source=0, weight='weight')
    nx_distances = np.array([nx_distances[key] for key in sorted(nx_distances.keys())])
    nx_distances[nx_distances == 0] = np.inf
    print(nx_distances)


if __name__ == "__main__":
    main()
