from fei.ppds import Thread


def tasks(thread_id, name):
    """"""
    print(f"{name} (id: {thread_id}) is running")


def main():
    """Creates 2 threads demonstrating the serialization of executing a specific task."""
    n_threads = 2
    names = ["Jano","Fero"]

    threads = [Thread(tasks, i, names[i]) for i in range(n_threads)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main()