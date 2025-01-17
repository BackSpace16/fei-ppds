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

        Keyword arguments:
        semaphore -- signalize after barrier unlocking (default None)
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
        self.boarded = Semaphore(0)
        self.board_queue = Semaphore(0)
        self.board_barrier = SimpleBarrier(CAPACITY)

        self.unboarded = Semaphore(0)
        self.unboard_queue = Semaphore(0)
        self.unboard_barrier = SimpleBarrier(CAPACITY)


def load():
    print(f"Train is empty, ready for boarding.")


def run():
    print(f"Train is full, departing.")
    sleep(5)
    print(f"Train arrived.")


def unload():
    print(f"Train is ready for unloading.")


def board(id):
    sleep((randint(0,20)+5)/10)
    print(f"Passenger {id} boarded.")


def unboard(id):
    sleep((randint(0,20)+5)/10)
    print(f"Passenger {id} unboarded.")


def train(shared):
    """Load passengers, run and unload passengers in loop."""
    while 42:
        load()
        shared.board_queue.signal(CAPACITY)
        shared.boarded.wait()
        run()
        unload()
        shared.unboard_queue.signal(CAPACITY)
        shared.unboarded.wait()


def passenger(id, shared):
    """Wait for train, then board, take a ride and unboard in loop."""
    while 42:
        sleep(randint(2,10))

        shared.board_queue.wait()
        board(id)
        shared.board_barrier.wait(shared.boarded)

        shared.unboard_queue.wait()
        unboard(id)
        shared.unboard_barrier.wait(shared.unboarded)


def main():
    """Simulate the roller coaster synchronization problem."""
    shared = Shared()
    threads = [Thread(passenger, i, shared) for i in range(N_PASSENGERS)]
    threads.append(Thread(train, shared))
    [t.join() for t in threads]


if __name__ == '__main__':
    main()