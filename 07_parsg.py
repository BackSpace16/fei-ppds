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
assert NRA % nproc == 0, f"#MPI_nodes should divide #rows of matrix A"

print(f"{rank}: Starting parallel matrix multiplication example...")
print(f"{rank}: Using matrix sizes A[{NRA}][{NCA}], B[{NCA}][{NCB}], C[{NRA}][{NCB}]")

A = None
B = None
rows = NRA // nproc
if rank == MASTER:
    print(f"{rank}: Initializing matrices A and B.")
    A = np.array([i+j for j in range(NRA) for i in range(NCA)]).reshape(nproc, NRA // nproc, NCA)
    B = np.array([i*j for j in range(NCA) for i in range(NCB)]).reshape(NCA, NCB)

A_loc = comm.scatter(A, root = MASTER)
B = comm.bcast(B, root = MASTER)

# Perform sequential matrix multiplication
C_loc = np.zeros((rows, NCB), dtype = int)
print(f"{rank}: Performing matrix multiplication...")
for i in range(rows):
    for j in range(NCB):
        for k in range(NCA):
            C_loc[i][j] += A_loc[i][k] * B[k][j]

# Combine results into matrix C
C = comm.gather(C_loc, root = MASTER)
if rank == MASTER:
    C = np.array([ss for s in C for ss in s])
    print(f"{rank}: Here is the result matrix:")
    print(C)

print(f"{rank}: Done.")
