import random
import numpy as np


LIST_LENGTH = 10
MIN_VALUE = 0
MAX_VALUE = 100
N_BUCKETS = 4


def sample_sort(data, p):

    # choose and sort samples
    samples = np.random.choice(data, p-1, replace=False)
    samples.sort()
    splitters = np.concatenate(([MIN_VALUE-1], samples, [MAX_VALUE+1]))
    print(splitters)

    # create buckets from samples
    buckets = [np.empty(0, dtype=int) for _ in range(len(splitters) - 1)]
    
    for a in data:
        j = 0
        while not (splitters[j] < a <= splitters[j+1]):
            j += 1
        buckets[j] = np.append(buckets[j], a)

    # sort buckets
    for b in buckets:
        b.sort()

    # concentrate buckets
    data = np.concatenate(buckets)
    return data


def main():
    list = np.random.randint(MIN_VALUE, MAX_VALUE, size=LIST_LENGTH)
    print(list)

    sorted_list = sample_sort(list, N_BUCKETS)

    print(sorted_list)


if __name__ == '__main__':
    main()
