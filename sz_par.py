import os
import csv
import numpy as np
from mpi4py import MPI
from sz import generate_adj_matrix, dijkstra


MASTER = 0

N_ATTEMPTS = 100
N_NODES = 100
MIN_WEIGHT = 1
MAX_WEIGHT = 10
EDGE_DENSITY = 0

CSV = f"data/{str(N_NODES)}_{str(EDGE_DENSITY)}_{N_ATTEMPTS}.csv"


def main():
    """Parallel version of dijkstra algorithm."""
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nproc = comm.Get_size()

    if rank == MASTER:
        times_par = []

    for t in range(N_ATTEMPTS):
        nproc_split = False
        if nproc > N_NODES:
            nproc_split = True
            comm = MPI.COMM_WORLD.Split(color=(rank < N_NODES))
            nproc = comm.Get_size()

        indices_modulo = N_NODES % nproc
        comm_tail = MPI.COMM_WORLD.Split(color=(rank < indices_modulo))

        indices = None
        indices_tail = None
        adj_matrix = None

        if rank == MASTER:
            start_time = MPI.Wtime()

            adj_matrix = generate_adj_matrix(N_NODES, MIN_WEIGHT, MAX_WEIGHT, EDGE_DENSITY)
            indices = np.array([i for i in range(N_NODES)])

            if indices_modulo != 0:
                indices_tail = indices[-(N_NODES % nproc) :]
                indices = indices[: -(N_NODES % nproc)]
                indices_tail = indices_tail.reshape(indices_modulo, 1)

            indices = indices.reshape(nproc, N_NODES // nproc)

        indices_loc = comm.scatter(indices, root=MASTER)
        if indices_modulo != 0 and rank < indices_modulo:
            indices_loc_tail = comm_tail.scatter(indices_tail, root=MASTER)
        adj_matrix = comm.bcast(adj_matrix, root=MASTER)

        if (not nproc_split or 
                nproc_split and nproc - N_NODES == 0 and rank < nproc):

            distances = []
            for i in indices_loc:
                distances.append(dijkstra(adj_matrix, i))

            distances = np.array(distances)
            all_distances = comm.gather(distances, root=MASTER)
            
            if indices_modulo != 0 and rank < indices_modulo:
                
                distances_tail = []
                for i in indices_loc_tail:
                    distances_tail.append(dijkstra(adj_matrix, i))

                distances_tail = np.array(distances_tail)
                distances_tail = comm_tail.gather(distances_tail, root=MASTER)

                if rank == MASTER:
                    distances_tail = np.array([ss for s in distances_tail for ss in s])
        
        if rank == MASTER:
            distances_par = np.array([ss for s in all_distances for ss in s])
            if indices_modulo != 0:
                distances_par = np.vstack([distances_par, distances_tail])

            end_time = MPI.Wtime()
            elapsed_time_par = end_time - start_time
            times_par.append(elapsed_time_par)

            print(f"{t}:\t{elapsed_time_par:.4f} seconds")

    if rank == MASTER:
        mean_time_par = np.mean(times_par)
        median_time_par = np.median(times_par)
        std_deviation_par = np.std(times_par)
        stats_par = [mean_time_par, median_time_par, std_deviation_par]

        print(30*"-")
        print(f"Mean time:\t{mean_time_par:.4f} seconds")
        print(f"Median time:\t{median_time_par:.4f} seconds")
        print(f"Std. deviation:\t{std_deviation_par:.4f} seconds")

        csv_file = CSV
        if not os.path.isfile(csv_file):
            with open(csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Index'])
                writer.writerows([[str(i)] for i in range(N_ATTEMPTS)])
                writer.writerows([["Mean"],["Median"],["Std_dev"]])

        existing_data = []
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            existing_data = [row for row in reader]

        existing_data_stat = existing_data[-3:]
        existing_data = existing_data[:-3]
        for i, row in enumerate(existing_data):
            row.append(times_par[i])
        for i, row in enumerate(existing_data_stat):
            row.append(stats_par[i])

        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header + ['Time_'+str(nproc)])
            writer.writerows(existing_data)
            writer.writerows(existing_data_stat)


if __name__ == "__main__":
    main()
