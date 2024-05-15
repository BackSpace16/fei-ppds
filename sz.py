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


def main():
    adj_matrix = load_adj_matrix("inputs/input2.txt")
    print(adj_matrix)


if __name__ == "__main__":
    main()
