from numba import cuda
import numpy as np


ARRAY_LENGTH = 10000
MIN_VALUE = 0
MAX_VALUE = 100
N_BUCKETS = 100
MAX_THREADS = 32


@cuda.jit
def insertion_sort(arr):
    n = arr.shape[0]
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


@cuda.jit
def sort_evenly(data, bucket_size):
    pos = cuda.grid(1)
    start = pos * bucket_size
    end = start + bucket_size

    #print("Thread", pos, ":", start, "-", end)
    if pos < data.shape[0]:
        insertion_sort(data[start:end])

        
@cuda.jit
def sort_splitters(data, lengths):
    pos = cuda.grid(1)
    start = lengths[pos]
    end = lengths[pos+1]

    #print("Thread", pos, ":", start, "-", end)
    if pos < data.shape[0]:
        insertion_sort(data[start:end])


def sample_sort(data, p):
    blocks = N_BUCKETS // MAX_THREADS + 1
    if N_BUCKETS < MAX_THREADS:
        threads = N_BUCKETS
    else:
        threads = MAX_THREADS

    bucket_size = data.size // N_BUCKETS
    if data.size % N_BUCKETS != 0:
        bucket_size += 1
    
    print("\nBlocks and threads:")
    print((blocks,threads))

    # divide array to N_BUCKET parts and sort them
    #print("\nThread part division:")
    data_mem = cuda.to_device(data)
    sort_evenly[blocks,threads](data_mem, bucket_size)
    data = data_mem.copy_to_host()

    print("\nSorted parts:")
    print(data)

    # choose samples from sorted parts
    sample_distance = bucket_size // N_BUCKETS + 1
    samples = np.empty(0, dtype=int)
    for i in range(0,N_BUCKETS):
        for j in range(0,N_BUCKETS-1):
            index = i*bucket_size + j*sample_distance+sample_distance-1
            if index < data.size:
                samples = np.append(samples, data[index])

    # sort samples and choose splitters from samples
    samples = np.sort(samples)
    choosing_index = N_BUCKETS//2
    splitters = np.empty(0, dtype=int)
    for i in range(0,samples.size,N_BUCKETS):
        if i+choosing_index < samples.size:
            splitters = np.append(splitters,samples[i+choosing_index])
    splitters = np.concatenate(([MIN_VALUE-1], splitters, [MAX_VALUE+1]))
    print("\nSplitters:")
    print(splitters)

    # create buckets from samples
    buckets = [np.empty(0, dtype=int) for _ in range(len(splitters) - 1)]
    
    for a in data:
        j = 0
        while not (splitters[j] < a <= splitters[j+1]):
            j += 1
        buckets[j] = np.append(buckets[j], a)

    lengths = np.empty(0,dtype=int)
    lengths = np.append(lengths,0)
    for b in buckets:
        lengths = np.append(lengths,lengths[-1]+b.size)

    print("\nBucket lengths (splitter indices):")
    print(lengths)
    print("\nBuckets:")
    print(buckets)

    # sort buckets
    data = np.concatenate(buckets)

    #print("\nThread bucket division:")
    data_mem = cuda.to_device(data)
    sort_splitters[blocks,threads](data_mem, lengths)
    data = data_mem.copy_to_host()

    return data


def main():
    list = np.random.randint(MIN_VALUE, MAX_VALUE, size=ARRAY_LENGTH)
    
    print("Data:")
    print(list)

    start_event = cuda.event()
    end_event = cuda.event()

    start_event.record()
    sorted_list = sample_sort(list, N_BUCKETS)
    end_event.record()
    end_event.synchronize()
    print(f'Kernel execution time in milliseconds: {cuda.event_elapsed_time(start_event, end_event):.2f}')

    print("\nResult:")
    print(sorted_list)


if __name__ == '__main__':
    main()
