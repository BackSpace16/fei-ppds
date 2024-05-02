from queue import Queue
from time import sleep, time


class Scheduler:
    def __init__(self):
        """Initialise queue of tasks."""
        self.tasks = Queue()

    def add_job(self, iterator):
        """Add task to queue."""
        self.tasks.put(iterator)

    def start(self):
        """Get task from queue and call next() on its generator object
        then put it back into queue.
        """
        while not self.tasks.empty():
            task = self.tasks.get()
            try:
                next(task)
                self.tasks.put(task)
            except StopIteration:
                print("Task completed.")


def coprogram1(n):
    """Count to n and print numbers"""
    print(f"Coprogram 1: starting")
    i = 0
    while i < n:
        sleep(0.5)
        print(f"Coprogram 1: {i}")
        yield
        i += 1


def coprogram2(i, n):
    """Print powers of two from i to n."""
    print(f"Coprogram 2: starting")
    while i < n:
        sleep(0.5)
        print(f"Coprogram 2: {i}")
        i = 1 if i == 0 else i * 2
        yield


def coprogram3(t):
    """Print elapsed time in seconds.
    
    Keyword arguments:
    t -- durration from start to stop in seconds
    """
    print(f"Coprogram 3: starting")
    start_time = time()
    while True:
        sleep(0.5)
        print(f"Coprogram 3: {(time() - start_time):.4f}s elapsed")
        if time() - start_time > t:
            break
        yield


def main():
    """Run 3 different coprograms through scheduler."""
    scheduler = Scheduler()

    task1 = coprogram1(5)
    task2 = coprogram2(1,5000)
    task3 = coprogram3(30)

    scheduler.add_job(task1)
    scheduler.add_job(task2)
    scheduler.add_job(task3)

    scheduler.start()


if __name__ == "__main__":
    main()
