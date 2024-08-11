import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

csv_files = ['500_times_C[48,48]_par.csv',
             '500_times_C[48,48]_parsg.csv',
             '500_times_C[96,96]_par.csv',
             '500_times_C[96,96]_parsg.csv',
             '100_times_C[192,192]_par.csv',
             '100_times_C[192,192]_parsg.csv',
             '25_times_C[432,432]_par.csv',
             '25_times_C[432,432]_parsg.csv',
             '25_times_C[432,48]_par.csv',
             '25_times_C[432,48]_parsg.csv',
             '25_times_C[48,432]_par.csv',
             '25_times_C[48,432]_parsg.csv']

names = ['C[48,48]_par',
         'C[48,48]_parsg',
         'C[96,96]_par',
         'C[96,96]_parsg',
         'C[192,192]_par',
         'C[192,192]_parsg',
         'C[432,432]_par',
         'C[432,432]_parsg',
         'C[432,48]_par',
         'C[432,48]_parsg',
         'C[48,432]_par',
         'C[48,432]_parsg']

data = []
stats = []
for i in range(len(csv_files)):
    df = pd.read_csv("data/"+csv_files[i])
    sorted_column_names = sorted([col for col in df.columns if col != 'Index'], key=lambda x: int(x.split('_')[1]))
    df_sorted = df.reindex(columns=['Index'] + sorted_column_names)

    stats.append(df_sorted.iloc[-3:])
    data.append(df_sorted.iloc[:-3])
    

for i in range(0,len(data)-11):
    plt.figure(figsize=(12, 6))
    for col in data[i].columns:
        if col != 'Index':
            plt.plot(data[i]['Index'], data[i][col], label="nproc: "+col.split('_')[1])
    plt.title(names[i])

    plt.xlabel('Index of attempt')
    plt.ylabel('Time (s)')
    plt.legend()
    plt.grid(True)
    x_labels = np.arange(0, len(data[i]), step=20)  # Napríklad vynechajme každé 5. označenie
    plt.xticks(x_labels)
    plt.show()


plt.figure(figsize=(6, 6))
for i in range(len(stats)-4):
    mean_row = stats[i].loc[stats[i]['Index'] == 'Mean'].iloc[:, 1:].values[0]
    column_names = stats[i].columns[1:]
    column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
    column_labels = [int(col.split('_')[1]) for col in column_names]
    plt.plot(column_labels, mean_row, label=names[i], marker='o')
plt.xlabel('Number of Processes')
plt.ylabel('Mean Time (s)')
plt.title('All square matrices')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(6, 6))
for i in range(len(stats)-8):
    mean_row = stats[i].loc[stats[i]['Index'] == 'Mean'].iloc[:, 1:].values[0]
    column_names = stats[i].columns[1:]
    column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
    column_labels = [int(col.split('_')[1]) for col in column_names]
    plt.plot(column_labels, mean_row, label=names[i], marker='o')
plt.xlabel('Number of Processes')
plt.ylabel('Mean Time (s)')
plt.title('C[48,48] vs C[96,96]')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(6, 6))
for i in range(2):
    mean_row = stats[i].loc[stats[i]['Index'] == 'Mean'].iloc[:, 1:].values[0]
    column_names = stats[i].columns[1:]
    column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
    column_labels = [int(col.split('_')[1]) for col in column_names]
    plt.plot(column_labels, mean_row, label=names[i], marker='o')
for i in range(8,len(stats)):
    mean_row = stats[i].loc[stats[i]['Index'] == 'Mean'].iloc[:, 1:].values[0]
    column_names = stats[i].columns[1:]
    column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
    column_labels = [int(col.split('_')[1]) for col in column_names]
    plt.plot(column_labels, mean_row, label=names[i], marker='o')
plt.xlabel('Number of Processes')
plt.ylabel('Mean Time (s)')
plt.title('C[48,48] vs C[432,48] vs C[48,432]')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(6, 6))
for i in range(2):
    mean_row = stats[i].loc[stats[i]['Index'] == 'Mean'].iloc[:, 1:].values[0]
    column_names = stats[i].columns[1:]
    column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
    column_labels = [int(col.split('_')[1]) for col in column_names]
    plt.plot(column_labels, mean_row, label=names[i], marker='o')
plt.xlabel('Number of Processes')
plt.ylabel('Mean Time (s)')
plt.title('C[48,48] Matrix')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(6, 6))
for i in range(6,8):
    mean_row = stats[i].loc[stats[i]['Index'] == 'Mean'].iloc[:, 1:].values[0]
    column_names = stats[i].columns[1:]
    column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
    column_labels = [int(col.split('_')[1]) for col in column_names]
    plt.plot(column_labels, mean_row, label=names[i], marker='o')
plt.xlabel('Number of Processes')
plt.ylabel('Mean Time (s)')
plt.title('C[432,432] Matrix')
plt.legend()
plt.grid(True)
plt.show()
