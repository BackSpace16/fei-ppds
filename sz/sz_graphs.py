import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    """Plot graphs with data from csv files."""
    csv_files = ['50_0_500.csv',
                 '100_0_100.csv',
                 '100_33_100.csv',
                 '100_66_100.csv',
                 '100_100_100.csv',
                 '250_0_50.csv',
                 '500_0_10.csv',
                 '1000_0_5.csv']

    names = ['50_0_500',
             '100_0_100',
             '100_33_100',
             '100_66_100',
             '100_100_100',
             '250_0_50',
             '500_0_10',
             '1000_0_5']

    data = []
    stats = []

    for i in range(len(csv_files)):
        df = pd.read_csv("data/"+csv_files[i])
        column_names = [col for col in df.columns if col != 'Index']
        sorted_column_names = sorted(column_names,
                                     key=lambda x: int(x.split('_')[1]))
        df_sorted = df.reindex(columns=['Index'] + sorted_column_names)

        stats.append(df_sorted.iloc[-3:])
        data.append(df_sorted.iloc[:-3])

    for i in range(0, 1):
        plt.figure(figsize=(12, 6))
        for col in data[i].columns:
            if col != 'Index':
                index_values = data[i]['Index']
                column_values = data[i][col]
                label = "nproc: " + col.split('_')[1]
                plt.plot(index_values, column_values, label=label)

        plt.title(names[i])
        plt.xlabel('Index of attempt')
        plt.ylabel('Time (s)')
        plt.legend()
        plt.grid(True)
        x_labels = np.arange(0, len(data[i]), step=20)
        plt.xticks(x_labels)
        plt.show()

    plt.figure(figsize=(6, 6))
    for i in range(2):
        median_row = stats[i].loc[stats[i]['Index'] == 'Median']
        median_values = median_row.iloc[:, 1:]
        median_row = median_values.values[0]

        column_names = stats[i].columns[1:]
        column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
        column_labels = [int(col.split('_')[1]) for col in column_names]

        plt.plot(column_labels, median_row, label=names[i], marker='o')

    plt.xlabel('Number of Processes')
    plt.ylabel('Median Time (s)')
    plt.title('Small graphs')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(6, 6))
    for i in range(2):
        median_row = stats[i].loc[stats[i]['Index'] == 'Median']
        median_values = median_row.iloc[:, 1:]
        median_row = median_values.values[0]

        column_names = stats[i].columns[1:]
        column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
        column_labels = [int(col.split('_')[1]) for col in column_names]

        plt.plot(column_labels, median_row, label=names[i], marker='o')

    for i in range(4, 6):
        median_row = stats[i].loc[stats[i]['Index'] == 'Median']
        median_values = median_row.iloc[:, 1:]
        median_row = median_values.values[0]

        column_names = stats[i].columns[1:]
        column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
        column_labels = [int(col.split('_')[1]) for col in column_names]

        plt.plot(column_labels, median_row, label=names[i], marker='o')

    plt.xlabel('Number of Processes')
    plt.ylabel('Median Time (s)')
    plt.title('50 vs 100 vs 250 vertices graphs')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(6, 6))
    for i in range(1, 5):
        median_row = stats[i].loc[stats[i]['Index'] == 'Median']
        median_values = median_row.iloc[:, 1:]
        median_row = median_values.values[0]

        column_names = stats[i].columns[1:]
        column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
        column_labels = [int(col.split('_')[1]) for col in column_names]

        plt.plot(column_labels, median_row, label=names[i], marker='o')

    plt.xlabel('Number of Processes')
    plt.ylabel('Median Time (s)')
    plt.title('100 vertices, different edge density')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(6, 6))
    for i in range(2):
        median_row = stats[i].loc[stats[i]['Index'] == 'Median']
        median_values = median_row.iloc[:, 1:]
        median_row = median_values.values[0]

        column_names = stats[i].columns[1:]
        column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
        column_labels = [int(col.split('_')[1]) for col in column_names]

        plt.plot(column_labels, median_row, label=names[i], marker='o')

    for i in range(5, 8):
        median_row = stats[i].loc[stats[i]['Index'] == 'Median']
        median_values = median_row.iloc[:, 1:]
        median_row = median_values.values[0]

        column_names = stats[i].columns[1:]
        column_names = sorted(column_names, key=lambda x: int(x.split('_')[1]))
        column_labels = [int(col.split('_')[1]) for col in column_names]

        plt.plot(column_labels, median_row, label=names[i], marker='o')

    plt.xlabel('Number of Processes')
    plt.ylabel('Median Time (s)')
    plt.title('All graphs')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
