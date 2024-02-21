from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore


N_DINER = 7
POT_CAPACITY = 5


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
        self.pot = Mutex()
        self.portions = 0
        self.barrier = SimpleBarrier(N_DINER)
        self.chef = Semaphore(0)
        self.chef_done = Semaphore(0)


def diner(thread_id, shared):
    """Diner consumes dinner."""
    sleep(randint(1,10))
    print(f"{thread_id} dorazil k obedu")
    shared.barrier.wait()
    print(f"{thread_id} vypustili")
    
    shared.pot.lock()
    if shared.portions > 0:
        print(f"{thread_id} si bere jedlo")
        shared.portions -= 1
    else:
        print(f"{thread_id} zistil že hrniec je prázdny, volá kuchárovi")
        shared.chef.signal()
        shared.chef_done.wait()
        print(f"{thread_id} si bere jedlo")
        shared.portions -= 1
    shared.pot.unlock()


def chef(shared):
    """Chef cooks meal for diners."""
    while 42:
        shared.chef.wait()
        shared.portions += POT_CAPACITY
        print("kuchar doplnil hrniec")
        shared.chef_done.signal()


def main():
    """Create threads representing diners and chef thread with defined tasks."""
    shared = Shared()
    threads = [Thread(diner, i, shared) for i in range(N_DINER)]
    threads.append(Thread(chef, shared))
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
