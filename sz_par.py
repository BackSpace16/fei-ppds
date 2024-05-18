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
        par_distances = comm.gather(distances, root=MASTER)
        
        if indices_modulo != 0 and rank < indices_modulo:
            
            distances_tail = []
            for i in indices_loc_tail:
                distances_tail.append(dijkstra(adj_matrix, i))

            distances_tail = np.array(distances_tail)
            distances_tail = comm_tail.gather(distances_tail, root=MASTER)

            if rank == MASTER:
                distances_tail = np.array([ss for s in distances_tail for ss in s])
    
    if rank == MASTER:
        par_distances = np.array([ss for s in par_distances for ss in s])
        if indices_modulo != 0:
            par_distances = np.vstack([par_distances, distances_tail])

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
