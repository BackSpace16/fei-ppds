from fei.ppds import Thread


N_DINER = 7


class Shared:
    """Shared class among multiple threads."""
    def __init__(self):
        """Initialise."""
        # TODO implement
        pass


def diner(thread_id):
    """Diner consumes dinner."""
    # TODO implement
    pass


def chef():
    """Chef cooks meal for diners."""
    # TODO implement
    pass


def main():
    """Create threads representing diners and chef thread with defined tasks."""
    threads = [Thread(diner, i) for i in range(N_DINER)]
    threads.append(Thread(chef))
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
