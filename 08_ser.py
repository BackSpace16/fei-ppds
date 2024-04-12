import numpy as np
from numba import cuda


ARRAY_LENGTH = 100
MIN_VALUE = 0
MAX_VALUE = 100


def insertion_sort(arr):
    n = arr.shape[0]
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
    return arr


def main():
    list = np.random.randint(MIN_VALUE, MAX_VALUE, size=ARRAY_LENGTH)
    
    print("Data:")
    print(list)

    start_event = cuda.event()
    end_event = cuda.event()

    start_event.record()
    sorted_list = insertion_sort(list)
    end_event.record()
    end_event.synchronize()
    print(f'Kernel execution time in milliseconds: {cuda.event_elapsed_time(start_event, end_event):.2f}')

    print("\nResult:")
    print(sorted_list)


if __name__ == '__main__':
    main()
