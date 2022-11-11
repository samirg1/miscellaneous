from typing import Any, Callable
from random import randint

def default_key(a: Any) -> Any:
    """
    Default key function that simply returns the object inputted.
    - Input:
            - a (Any): An object.
    - Returns (Any): The object. 
    - Time Complexity: O(1).
    - Aux space complexity: O(1).
    """
    return a

def partition(lst: 'list[Any]', high: int, pivot: Any, key: Callable[[Any], Any] = default_key) -> 'tuple[int, int]':
    """
    Partitions a section of a list so that all elements greater than the pivot are to the right, and all elements smaller are to the left.
    - Input:
            - lst (list[Any]): The list to partition.
            - high (int): The highest point to partition to.
            - pivot (Any): The pivot to partition with respect to.
            - key (Callable[[Any], Any], optional): Function to map the pivot and any object in lst to the desired comparative value. Defaults to default_key.
    - Returns (tuple[int, int]): The indexes of the lower boundary (where the first pivot is) and the upper boundary (where the last pivot is), a list with no duplicates always has lower boundary == upper boundary. 
    - Time Complexity: O(N*k) where N is the amount of elements to partition and k is the complexity of key.
    - Aux space complexity: O(1).
    """
    pivot_value = key(pivot)
    lower_boundary = 0
    pointer = 0
    upper_boundary = high
    while pointer <= upper_boundary:
        pointer_value = key(lst[pointer])
        if pointer_value < pivot_value:
            lst[lower_boundary], lst[pointer] = lst[pointer], lst[lower_boundary]
            lower_boundary += 1
            pointer += 1
        elif pointer_value > pivot_value:
            lst[pointer], lst[upper_boundary] = lst[upper_boundary], lst[pointer]
            upper_boundary -= 1
        else:
            pointer += 1
    return lower_boundary, upper_boundary

def quick_select(lst: 'list[Any]', k: int, key: Callable[[Any], Any] = default_key, low: int = 0, high: int = None) -> Any:
    """
    Quickselect algortithm that selects the k'th biggest element of a section of a list using medians of medians to select its pivot.
    - Input:
            - lst (list[Any]): The list to find element.
            - k (int): The element to be searched for.
            - key (Callable[[Any], Any], optional): Function to map an object in lst to the desired comparative value. Defaults to default_key.
            - low (int, optional): The lowest index to check in. Defaults to 0.
            - high (int, optional): The highest index to check in. Defaults to None.
    - Returns (Any): The k'th biggest element in lst[low:high+1]. 
    - Time Complexity: O(N*k) where N is the amount of elements to check (high-low+1) and k is the complexity of key.
    - Aux space complexity: O(N).
    """
    high = len(lst) - 1 if high is None else high
    if low > high:
        return lst[k]
    pivot = medians_of_medians(lst, low, high, key)
    lower_boundary, upper_boundary = partition(lst, high, pivot, key)
    if k < lower_boundary:
        return quick_select(lst, k, key, low, lower_boundary-1)
    elif k > upper_boundary:
        return quick_select(lst, k, key, upper_boundary+1, high)
    else:
        return lst[k]

def create_sublists(lst: 'list[Any]', n: int, low: int = 0, high: int = None) -> 'list[list[Any]]':
    """
    Creates sublists of a list of a certain size.
    - Input:
            - lst (list[Any]): The list to sublist.
            - n (int): The size of the sublists.
            - low (int, optional): The index to start sublisting. Defaults to 0.
            - high (int, optional): The index to finish sublisting. Defaults to None.
    - Returns (list[list[Any]]): The sublists of size n of lst[low:high+1]. 
    - Time Complexity: O(N) where N is the amount of elements to search for (low-high+1).
    - Aux space complexity: O(N).
    """
    high = len(lst) - 1 if high is None else high
    sublists = []
    while low + n < high + 1:
        sublists.append(lst[low:low+n])
        low += n
    if low < high + 1:
        sublists.append(lst[low:low+(high-low+1)])
    return sublists

def medians_of_medians(lst: 'list[Any]', low: int, high: int, key: Callable[[Any], Any] = default_key) -> Any:
    """
    The famouns medians of medians algorithm that find a worst case 70:30 split median in a list.
    - Input:
            - lst (list[Any]): The list to find the median from.
            - low (int): The index to start looking from.
            - high (int): The index to finish looking.
            - key (Callable[[Any], Any], optional): Function mapping an object in lst to the desired comparative value. Defaults to default_key.
    - Returns (Any): The median of medians. 
    - Time Complexity: O(N*k) where N is amount of elements to search through (high-low+1) and k is the complexity of the key function.
    - Aux space complexity: O(N).
    """
    size = high - low + 1
    if size <= 5:
        return sorted(lst[low:high+1])[size//2]

    sublists = create_sublists(lst, 5, low, high)
    medians = [sub[len(sub)//2] for sub in sublists]
    return quick_select(medians, (len(medians)+1)//2, key)


def quick_sort(lst: 'list[Any]', key: Callable[[Any], Any] = default_key, low: int = 0, high: int = None) -> 'list[Any]':
    """
    Quick sort algorithm that uses quickselect to select its pivot.
    - Input:
            - lst (list[Any]): The list to sort.
            - key (Callable[[Any], Any], optional): Function mapping objects in the list to the desired comparative values. Defaults to default_key.
            - low (int, optional): The index to start sorting from. Defaults to 0.
            - high (int, optional): The index to finish sorting. Defaults to None.
    - Returns (list[Any]): Sorted lst[low:high+1]. 
    - Time Complexity: O(N*log(N)), where N is the length of the list (or high-low+1).
    - Aux space complexity: O(N*log(N)).
    """
    high = len(lst) - 1 if high is None else high
    if low < high:
        median = low + (high-low)//2
        pivot = quick_select(lst, median, key, low, high)
        lower_boundary, upper_boundary = partition(lst,  high, pivot, key)
        quick_sort(lst, key, low, lower_boundary-1)
        quick_sort(lst, key, upper_boundary+1, high)
    return lst

# TESTING
if __name__ == '__main__':
    from time import time
    start = time()
    for _ in range(1000):
        lst = [randint(0, 100) for _ in range(200)]
        cop = lst.copy()
        quick_sort(lst)
        assert lst == sorted(lst), \
            f'expected {sorted(lst)}, got {lst}, with {cop}'

    print('****REGULAR PASSED*****')
    print(time()-start)
    start = time()

    for _ in range(1000):
        tup_lst = [(randint(0, 100), randint(0, 100)) for _ in range(200)]
        check = randint(0, 1)
        f = lambda a: a[check]
        tup_cop = tup_lst.copy()
        quick_sort(tup_lst, key=f)  
        assert tup_lst == sorted(tup_lst, key=f), \
            f'expected {sorted(tup_lst, key=f)}, got {tup_lst}, with {tup_cop}'

    print('****OBJECTS PASSED*****')
    print(time()-start)
