import numpy as np


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


def main():
    adj_matrix = load_adj_matrix("inputs/input2.txt")
    print(adj_matrix)

    source = 0
    distances = dijkstra(adj_matrix, source)
    print(distances)


if __name__ == "__main__":
    main()
