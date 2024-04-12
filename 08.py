import random


N_BUCKETS = 4


def sample_sort(data, p):

    # choose and sort samples
    samples = random.sample(data, p-1)
    samples.sort()
    splitters = [-float('inf')] + samples + [float('inf')]

    # create buckets from samples
    buckets = [[] for _ in range(len(splitters) - 1)]
    
    for a in data:
        j = 0
        while not (splitters[j] < a <= splitters[j+1]):
            j += 1
        buckets[j].append(a)

    # sort buckets
    for b in buckets:
        b.sort()

    # concentrate buckets
    data = [item for sublist in buckets for item in sublist]
    return data


def main():
    list = [2,5,1,4,9,7]
    print(list)

    sorted_list = sample_sort(list, N_BUCKETS)

    print(sorted_list)


if __name__ == '__main__':
    main()
