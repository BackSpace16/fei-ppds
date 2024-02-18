from fei.ppds import Thread
from random import randint
from time import sleep


def sleeping(name):
    """Simulate sleeping with random durration between 3 to 6 seconds."""
    time = randint(3, 6)
    print(f"{name} fell asleep. He will be sleeping {time}s.")
    sleep(time)
    print(f"{name} woke up.")


def hygiene(name):
    """Simulate doing morning hygiene with random durration between 1 to 2 seconds."""
    time = randint(1, 2)
    print(f"{name} started doing his morning hygiene. He will be done in {time}s.")
    sleep(time)
    print(f"{name} finished his morning hygiene.")


def tasks(thread_id, name):
    """"""
    sleeping(name)
    hygiene(name)


def main():
    """Creates 2 threads demonstrating the serialization of executing a specific task."""
    n_threads = 2
    names = ["Jano","Fero"]

    threads = [Thread(tasks, i, names[i]) for i in range(n_threads)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main()