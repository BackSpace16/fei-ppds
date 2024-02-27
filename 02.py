from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore


N_DINER = 7
POT_CAPACITY = 10


class SimpleBarrier:
    def __init__(self, max_threads):
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)
        self.max_threads = max_threads
        self.counter = 0
        self.unlock_text = "Barrier unlocked."

    def set_unlock_text(self, text):
        self.unlock_text = text

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.max_threads:
            self.turnstile.signal(self.max_threads)
            self.counter = 0
            print(self.unlock_text)
        self.mutex.unlock()
        self.turnstile.wait()


class Shared:
    """Shared class among multiple threads."""
    def __init__(self):
        """Initialise shared variables."""
        self.pot = Mutex()
        self.portions = 10

        self.barrier = SimpleBarrier(N_DINER)
        self.barrier.set_unlock_text("All diners came to lunch.")
        self.barrier2 = SimpleBarrier(N_DINER)
        self.barrier2.set_unlock_text("All diners have their portion. They proceed to eat.")

        self.chef = Semaphore(0)
        self.chef_done = Semaphore(0)


def diner(thread_id, shared):
    """Diner consumes dinner."""
    while 16:
        sleep(randint(1,10))
        print(f"Diner {thread_id} came to lunch.")
        shared.barrier.wait()

        shared.pot.lock()
        if shared.portions <= 0:
            print(f"Diner {thread_id} realised the pot is empty. Calling chef.")
            shared.chef.signal()
            shared.chef_done.wait()

        print(f"Diner {thread_id} picked his portion.")
        shared.portions -= 1
        shared.pot.unlock()

        shared.barrier2.wait()
        sleep(5)
        print(f"Diner {thread_id} finished lunch.")


def chef(shared):
    """Chef cooks meal for diners."""
    while 42:
        shared.chef.wait()
        print("Chef is preparing food.")
        sleep(5)
        shared.portions += POT_CAPACITY
        print("Chef refilled the pot.")
        shared.chef_done.signal()


def main():
    """Create threads representing diners and chef thread with defined tasks."""
    shared = Shared()
    threads = [Thread(diner, i, shared) for i in range(N_DINER)]
    threads.append(Thread(chef, shared))
    [t.join() for t in threads]


if __name__ == '__main__':
    main()
