import numpy as np
from mpi4py import MPI
from sz import generate_adj_matrix, dijkstra, all_dijkstra


MASTER = 0
N_NODES = 100
MIN_WEIGHT = 1
MAX_WEIGHT = 10
EDGE_DENSITY = 0


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    nproc = comm.Get_size()
    
    indices = None
    adj_matrix = None

    if rank == MASTER:
        start_time = MPI.Wtime()
        indices = np.array([i for i in range(N_NODES)])
        adj_matrix = generate_adj_matrix(N_NODES, MIN_WEIGHT, MAX_WEIGHT, EDGE_DENSITY)
        indices = indices.reshape(nproc, N_NODES // nproc)
        
    indices_loc = comm.scatter(indices, root = MASTER)
    adj_matrix = comm.bcast(adj_matrix, root = MASTER)

    distances = []
    for i in indices_loc:
        distances.append(dijkstra(adj_matrix, i))

    distances = np.array(distances)
    par_distances = comm.gather(distances, root = MASTER)
    
    if rank == MASTER:
        par_distances = np.array([ss for s in par_distances for ss in s])
        par_distances = par_distances.reshape(N_NODES, N_NODES)

        end_time = MPI.Wtime()
        elapsed_time = end_time - start_time

        print(par_distances)
        print(f"parallel: {elapsed_time:.4f}s")

        # serial
        start_time = MPI.Wtime()

        ser_distances = all_dijkstra(adj_matrix, dijkstra)

        end_time = MPI.Wtime()
        elapsed_time = end_time - start_time

        print(ser_distances)
        print(f"serial: {elapsed_time:.4f}s")
        
        if np.array_equal(par_distances, ser_distances):
            print("Matice su rovnake")
        else:
            print("Chyba!!! Matice nie su rovnake")


if __name__ == "__main__":
    main()
