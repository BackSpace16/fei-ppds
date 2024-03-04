from fei.ppds import Thread


N_PASSENGERS = 20


class Shared:
    """Shared class among multiple threads."""
    def __init__(self):
        """Initialise shared variables."""


def train(id, shared):
    """ TODO """
    pass


def passenger(id, shared):
    """ TODO """
    pass


def main():
    """."""
    shared = Shared()
    threads = [Thread(passenger, i, shared) for i in range(N_PASSENGERS)]
    threads.append(Thread(train, shared))
    [t.join() for t in threads]


if __name__ == '__main__':
    main()