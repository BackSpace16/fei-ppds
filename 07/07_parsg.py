'''
(c) Michal Vizvary, 2024-04-06
Prevzate a upravene z poskytnuteho kodu cv.mat_parsg.py od:
    (c) Matus Jokay, 2024-03-27
    prevzate a upravene pre jazyk Python z:
        https://kurzy.kpi.fei.tuke.sk/pp/labs/pp_mm.c

'''


import numpy as np
from mpi4py import MPI
import matplotlib.pyplot as plt
import csv
import os


NRA = 24   # number of rows in matrix A
NCA = 48  # number of columns in matrix A
NCB = 48  # number of columns in matrix B


MASTER = 0
N_ATTEMPTS = 1
CSV = f"data/{N_ATTEMPTS}_times_C[{str(NRA)},{str(NCB)}]_parsg.csv"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nproc = comm.Get_size()

if rank == MASTER:
    times = []

for t in range(N_ATTEMPTS):
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
        #print(f"{rank}: Starting parallel matrix multiplication example...")
        #print(f"{rank}: Using matrix sizes A[{NRA}][{NCA}], B[{NCA}][{NCB}], C[{NRA}][{NCB}]")
        #print(f"{rank}: Initializing matrices A and B.")
        A = np.array([i+j for j in range(NRA) for i in range(NCA)]).reshape(NRA, NCA)

        # Divide tail part of matrix A if NRA % nproc != 0
        if rows_modulo != 0:
            A_tail = A[-rows_modulo:]
            A = A[:-rows_modulo]
            A_tail = A_tail.reshape(rows_modulo, 1, NCA)
        
        A = A.reshape(nproc, rows, NCA)
        B = np.array([i*j for j in range(NCA) for i in range(NCB)]).reshape(NCA, NCB)

        start_time = MPI.Wtime()
    A_loc = comm.scatter(A, root = MASTER)
    if rows_modulo != 0 and rank < rows_modulo:
        A_tail_loc = comm_tail.scatter(A_tail, root = MASTER)
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
        
        end_time = MPI.Wtime()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        #print(f"{rank}: Here is the result matrix:")
        #print(C)
        print(f"{t} It took {elapsed_time} seconds")

    #print(f"{rank}: Done.")
    
if rank == MASTER:
    mean_time = np.mean(times)
    median_time = np.median(times)
    std_deviation = np.std(times)
    stats = [mean_time,median_time,std_deviation]

    print("Mean time:", mean_time)
    print("Median time:", median_time)
    print("Standard deviation:", std_deviation)
    plt.bar(range(len(times)), times)
    plt.xlabel('Measurement')
    plt.ylabel('Time (seconds)')
    plt.title('Time Measurements')
    plt.show()

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
        row.append(times[i])
    for i, row in enumerate(existing_data_stat):
        row.append(stats[i])

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header + ['Time_'+str(nproc)])
        writer.writerows(existing_data)
        writer.writerows(existing_data_stat)