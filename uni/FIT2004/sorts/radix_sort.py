from typing import Any, Callable
from counting_sort import counting_sort, default_key, SupportsDunderInt

def get_digit(num: int, digit: int) -> int:
    """
    Gets a specific digit of an integer.

    Args:
        num (int): The integer to search in.
        digit (int): The digit to find. (0 is the rightmost digit)

    Returns:
        int: The (`digit`+1)'th rightmost digit in `num`. Returns 0 if `digit` exceeds amount of digits in `num`.

    Raises:
        ValueError: If digit < 0.

    Complexity:
        Time and space: O(1).
    """
    if digit < 0:
        raise ValueError('Digit must be greater than 0')
    return num // 10**digit % 10

def radix_sort(lst: 'list[Any]', key: Callable[[SupportsDunderInt|Any], int] = default_key, reverse: bool = False) -> 'list[Any]':
    """
    Uses the Radix Sort technique to sort a list of integers with help from Counting Sort.

    Args:
        lst (list[Any]): List to be sorted.
        key (Callable[[Any], int], optional): Function mapping objects in the list to the integer value to sort by. Defaults to `default_key`.
        reverse (bool, optional): Whether or not to sort in descending order. Defaults to `False` (ascending).

    Returns:
        list[Any]: The sorted list.

    Complexity:
        Time: O(n*k*w/logn), w = max(width of integers), k = O(`key`).
        Space: O(n).
    """
    max_digits = len(str(max(lst, key=key))) # O(n*k)
    new_lst: list[Any] = [i for i in lst] # O(n)
    for d in range(max_digits): # O(n * k * w/logn)
        new_lst = counting_sort(new_lst, key=lambda n: get_digit(key(n), d)) # O(n*k)
    return new_lst[::-1] if reverse else new_lst        