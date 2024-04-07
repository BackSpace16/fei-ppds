'''
(c) Michal Vizvary, 2024-04-06
Prevzate a upravene z poskytnuteho kodu cv.mat_par.py od:
    (c) Matus Jokay, 2024-03-27
    prevzate a upravene pre jazyk Python z:
        https://kurzy.kpi.fei.tuke.sk/pp/labs/pp_mm.c

'''


import numpy as np
from mpi4py import MPI
import matplotlib.pyplot as plt
import csv
import os


NRA = 48  # number of rows in matrix A
NCA = 48  # number of columns in matrix A
NCB = 48  # number of columns in matrix B


MASTER = 0
N_ATTEMPTS = 25
CSV = f"data/{N_ATTEMPTS}_times_C[{str(NRA)},{str(NCB)}]_par.csv"

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nproc = comm.Get_size()
assert NRA % nproc == 0, f"#MPI_nodes should divide #rows of matrix A"

#print(f"{rank}: Starting parallel matrix multiplication example...")
#print(f"{rank}: Using matrix sizes A[{NRA}][{NCA}], B[{NCA}][{NCB}], C[{NRA}][{NCB}]")


if rank == MASTER:
    times = []

for t in range(N_ATTEMPTS):
    rows = NRA // nproc
    if rank == MASTER:
        #print(f"{rank}: Initializing matrices A and B.")
        A = np.array([i+j for j in range(NRA) for i in range(NCA)]).reshape(NRA, NCA)
        B = np.array([i*j for j in range(NCA) for i in range(NCB)]).reshape(NCA, NCB)

        start_time = MPI.Wtime()
        for proc in range(nproc):
            if proc == MASTER:
                A_loc = A[proc*rows:proc*rows+rows]
                continue
            comm.send(A[proc*rows:proc*rows+rows], dest = proc)
    else:
        A_loc = comm.recv()
        B = None

    B = comm.bcast(B, root = MASTER)

    # Perform sequential matrix multiplication
    C_loc = np.zeros((rows, NCB), dtype = int)
    #print(f"{rank}: Performing matrix multiplication...")
    for i in range(rows):
        for j in range(NCB):
            for k in range(NCA):
                C_loc[i][j] += A_loc[i][k] * B[k][j]


    # Combine results into matrix C
    C = np.zeros((NRA, NCB), dtype = int)
    if rank == MASTER:
        for proc in range(nproc):
            if proc == MASTER:
                C[proc*rows:proc*rows+rows] = C_loc
                continue
            C[proc*rows:proc*rows+rows] = comm.recv(source = proc)
            
        end_time = MPI.Wtime()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        #print(f"{rank}: Here is the result matrix:")
        #print(C)
        print(f"{t} It took {elapsed_time} seconds")
    else:
        comm.send(C_loc, dest = MASTER)

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