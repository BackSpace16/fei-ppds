from fei.ppds import Thread, Semaphore
from random import randint
from time import sleep


class Shared:
    """Class Shared is used for sharing a value among multiple threads."""
    def __init__(self):
        """Initializes the calling to False."""
        self.call = Semaphore(0)


def sleeping(name):
    """Simulate sleeping with random durration between 3 to 6 seconds."""
    time = randint(3, 6)
    print(f"{name} fell asleep. He will be sleeping {time}s.")
    sleep(time)
    print(f"{name} woke up.")


def hygiene(name):
    """Simulate doing morning hygiene with
    random durration between 1 to 2 seconds.
    """
    time = randint(1, 2)
    print(f"{name} started doing his morning hygiene. "
          f"He will be done in {time}s.")
    sleep(time)
    print(f"{name} finished his morning hygiene.")


def call(shared, name):
    """Simulate calling and waiting for response."""
    shared.call.signal()
    print(f"{name} is calling.")


def recieve_call(shared, name):
    """Simulate waiting for call and answering."""
    print(f"{name} waiting for a call.")
    shared.call.wait()
    print(f"{name} recieved call.")


def eating(name):
    """Simulate eating with random durration between 1 to 2 seconds."""
    time = randint(1, 2)
    print(f"{name} started eating. He will be done in {time}s.")
    sleep(time)
    print(f"{name} finished eating.")


def tasks(shared, thread_id, name):
    """Simulate given tasks, 
    ensure executing eating task by first
    thread before second thread
    """
    sleeping(name)
    hygiene(name)
    if thread_id > 0:
        recieve_call(shared, name)
    eating(name)
    if thread_id == 0:
        call(shared, name)


def main():
    """Create 2 threads demonstrating the serialization
    of executing a specific task.
    """
    N_THREADS = 2
    names = ["Jano","Fero"]

    shared = Shared()
    threads = [Thread(tasks, shared, i, names[i]) for i in range(N_THREADS)]
    [t.join() for t in threads]


if __name__ == '__main__':
    main()