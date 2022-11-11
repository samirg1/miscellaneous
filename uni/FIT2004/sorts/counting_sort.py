from abc import abstractmethod
from typing import Any, Callable, TypeVar

class SupportsInt:
    @abstractmethod
    def __int__(self) -> int: ...
    
SupportsDunderInt = TypeVar("SupportsDunderInt", bound=SupportsInt)

def default_key(a: SupportsDunderInt) -> int:
    """
    Default key function for counting sort.

    Args:
        a (Any): Object to extract int from.

    Returns:
        int: Integer extracted from Object.

    Complexity:
        Time and space: O(1).
    """
    return int(a)
    
def counting_sort(lst: 'list[Any]', /, *, key: Callable[[SupportsDunderInt|Any], int] = default_key, reverse: bool = False) -> list[Any]:
    """
    Counting sort implementation.

    Args:
        lst (Collection[Any]): Collection to sort. 
         key (Callable[[Any], int], optional): Function mapping objects in the list to the integer value to sort by. Defaults to `lambda` a: a.
        reverse (bool, optional): Reverse the order of sorting or not. Defaults to `False` (ascending order).

    Returns:
        Collection[Any]: Sorted collection.

    Complexity:
        Time: O(n*k+u), n=len(`lst`), k = O(`key`), u = domain of `lst`.
        Space: O(n+u).
    """
    minimum: int = key(min(lst, key=key)) # O(n*k)
    maximum: int = key(max(lst, key=key)) # O(n*k)
    domain: int = maximum - minimum # O(1)

    count: list[int] = [0 for _ in range(domain+1)] # O(u)
    for obj in lst: # O(n*k)
        count[key(obj)-minimum] += 1 # O(k)

    position: list[int] = [1] # O(1)
    for i in range(1, len(count)): # O(u)
        position.append(position[i-1] + count[i-1]) # O(1)

    output: list[Any] = [None for _ in range(len(lst))] # O(n)
    for obj in lst: # O(n*k)
        output[position[key(obj)-minimum]-1] = obj # O(k)
        position[key(obj)-minimum] += 1 # O(k)
    return output[::-1] if reverse else output

lst = [5, 2, 3, 1, 6, 1, 6]
print(counting_sort(lst, reverse=True))