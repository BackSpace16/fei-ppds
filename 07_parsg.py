'''
(c) Michal Vizvary, 2024-04-06
Prevzate a upravene z poskytnuteho kodu cv.mat_parsg.py od:
    (c) Matus Jokay, 2024-03-27
    prevzate a upravene pre jazyk Python z:
        https://kurzy.kpi.fei.tuke.sk/pp/labs/pp_mm.c

'''


import numpy as np
from mpi4py import MPI


NRA = 32  # number of rows in matrix A
NCA = 15  # number of columns in matrix A
NCB = 7   # number of columns in matrix B


MASTER = 0

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nproc = comm.Get_size()

if nproc > NRA:
    comm = MPI.COMM_WORLD.Split(color=(rank < NRA))
    nproc = comm.Get_size()

rows = NRA // nproc
rows_modulo = NRA % nproc

comm_tail = MPI.COMM_WORLD.Split(color=(rank < rows_modulo))

A = None
A_tail = None
B = None

if rank == MASTER:
    print(f"{rank}: Starting parallel matrix multiplication example...")
    print(f"{rank}: Using matrix sizes A[{NRA}][{NCA}], B[{NCA}][{NCB}], C[{NRA}][{NCB}]")
    print(f"{rank}: Initializing matrices A and B.")
    A = np.array([i+j for j in range(NRA) for i in range(NCA)]).reshape(NRA, NCA)

    # Divide tail part of matrix A if NRA % nproc != 0
    if rows_modulo != 0:
        A_tail = A[-rows_modulo:]
        A = A[:-rows_modulo]
        A_tail = A_tail.reshape(rows_modulo, 1, NCA)
    
    A = A.reshape(nproc, rows, NCA)
    B = np.array([i*j for j in range(NCA) for i in range(NCB)]).reshape(NCA, NCB)

A_loc = comm.scatter(A, root = MASTER)
B = comm.bcast(B, root = MASTER)

if rank < nproc:
    # Perform sequential matrix multiplication
    C_loc = np.zeros((rows, NCB), dtype = int)
    for i in range(rows):
        for j in range(NCB):
            for k in range(NCA):
                C_loc[i][j] += A_loc[i][k] * B[k][j]

    # Combine results into matrix C
    C = comm.gather(C_loc, root = MASTER)
    if rank == MASTER:
        C = np.array([ss for s in C for ss in s])

    # Perform sequential matrix multiplication on tail part if needed
    if rows_modulo != 0 and rank < rows_modulo:
        A_tail_loc = comm_tail.scatter(A_tail, root = MASTER)
        C_tail_loc = np.zeros((1, NCB), dtype = int)

        for j in range(NCB):
            for k in range(NCA):
                C_tail_loc[0][j] += A_tail_loc[0][k] * B[k][j]

        C_tail = comm_tail.gather(C_tail_loc, root = MASTER)
        if rank == MASTER:
            C_tail = np.array([ss for s in C_tail for ss in s])

# Add tail part into final matrix C if needed
if rank == MASTER:
    if rows_modulo != 0:
        C = np.vstack([C, C_tail])
    print(f"{rank}: Here is the result matrix:")
    print(C)

print(f"{rank}: Done.")
