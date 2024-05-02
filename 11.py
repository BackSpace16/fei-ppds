from queue import Queue
from time import sleep


class Scheduler:
    def __init__(self):
        self.tasks = Queue()

    def add_job(self, iterator):
        self.tasks.put(iterator)

    def start(self):
        while not self.tasks.empty():
            task = self.tasks.get()
            try:
                next(task)
                self.tasks.put(task)
            except StopIteration:
                print("Task completed.")


def coprogram1(n):
    i = 0
    while i < n:
        sleep(0.5)
        print(f"Coprogram 1: {i}")
        yield
        i += 1


def main():
    scheduler = Scheduler()

    task1 = coprogram1(5)
    task2 = coprogram1(10)
    task3 = coprogram1(30)

    scheduler.add_job(task1)
    scheduler.add_job(task2)
    scheduler.add_job(task3)

    scheduler.start()


if __name__ == "__main__":
    main()
