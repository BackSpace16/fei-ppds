from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore


N_DINER = 7


class SimpleBarrier:
    def __init__(self, max_threads):
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)
        self.max_threads = max_threads
        self.counter = 0

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.max_threads:
            self.turnstile.signal(self.max_threads)
        self.mutex.unlock()
        self.turnstile.wait()


class Shared:
    """Shared class among multiple threads."""
    def __init__(self):
        """Initialise."""
        self.barrier = SimpleBarrier(N_DINER)
        # TODO implement
        pass


def diner(thread_id, shared):
    """Diner consumes dinner."""
    # TODO implement
    sleep(randint(1,10))
    print(f"{thread_id} dorazil k bariere")
    shared.barrier.wait()
    print(f"{thread_id} vypustili")
    pass


def chef(shared):
    """Chef cooks meal for diners."""
    # TODO implement
    pass


def main():
    """Create threads representing diners and chef thread with defined tasks."""
    shared = Shared()
    threads = [Thread(diner, i, shared) for i in range(N_DINER)]
    threads.append(Thread(chef, shared))
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
