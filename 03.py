from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore


N_PASSENGERS = 20
CAPACITY = 8


class SimpleBarrier:
    def __init__(self, max_threads):
        """Initialise the barrier
        
        Keyword arguments:
        max_threads -- how many threads will synchronise
        """
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)
        self.max_threads = max_threads
        self.counter = 0
        self.unlock_text = None

    def set_unlock_text(self, text):
        """Set text to print after unlocking."""
        self.unlock_text = text

    def wait(self, semaphore = None):
        """Wait for synchronization.
        Counter counts number of threads,
        if they reach max_threads barrier unlocks
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.max_threads:
            self.turnstile.signal(self.max_threads)
            self.counter = 0
            if semaphore != None:
                semaphore.signal()
            if self.unlock_text != None:
                print(self.unlock_text)
        self.mutex.unlock()
        self.turnstile.wait()


class Shared:
    """Shared class among multiple threads."""
    def __init__(self):
        """Initialise shared variables."""
        self.barrier = SimpleBarrier(CAPACITY)
        self.barrier.set_unlock_text("bariera vypusta")
        self.boarded = Semaphore(0)
        self.boardQueue = Semaphore(0)


def train(shared):
    """ TODO """
    print(f"prisel vlacik")
    shared.boardQueue.signal(CAPACITY)
    print(f"caka vlacik")
    shared.boarded.wait()
    print(f"jede vlacik")
    pass


def passenger(id, shared):
    """ TODO """
    sleep(randint(2,10))
    print(f"{id} caka")
    shared.boardQueue.wait()
    print(f"{id} nastupil")
    shared.barrier.wait(shared.boarded)
    print(f"{id} vypustene")
    pass


def main():
    """."""
    shared = Shared()
    threads = [Thread(passenger, i, shared) for i in range(N_PASSENGERS)]
    threads.append(Thread(train, shared))
    [t.join() for t in threads]


if __name__ == '__main__':
    main()