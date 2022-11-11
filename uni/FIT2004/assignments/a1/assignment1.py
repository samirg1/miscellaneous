from typing import Any, Callable

def default_key(a: Any) -> int:
    """
    A default key function to map an object to an integer.
    - Input:
            - a (Any): The object to map.
    - Returns (int): The integer produced. 
    - Time Complexity: O(1).
    - Aux space complexity: O(1).
    """
    return int(a)
    
def counting_sort(lst: 'list[Any]', key: Callable[[Any], int] = default_key, reverse: bool = False) -> 'list[Any]':
    """
    Counting Sort implementation..
    - Input:
            - lst (list[Any]): The list to be sorted.
            - key (Callable[[Any], int], optional): Function to map the list objects to an integer value. Defaults to default_key.
            - reverse (bool, optional): Whether or not the list should be in non-increasing order. Defaults to False (non-decreasing).
    - Returns (list[Any]): The sorted list. 
    - Time Complexity: O(N*k+u), where N == len(lst), k == O(key) and u is the domain of lst.
    - Aux space complexity: O(N+u).
    """
    minimum: int = key(min(lst, key=key)) # O(N*k)
    maximum: int = key(max(lst, key=key)) # O(N*k)
    domain: int = maximum - minimum # O(1)

    count: list[int] = [0 for _ in range(domain+1)] # O(u)
    for obj in lst: # O(n*k)
        count[key(obj)-minimum] += 1 # O(k)

    position: list[int] = [1] # O(1)
    for i in range(1, len(count)): # O(u)
        position.append(position[i-1] + count[i-1]) # O(1)

    output: list[Any] = [None for _ in range(len(lst))] # O(N)
    for obj in lst: # O(N*k)
        output[position[key(obj)-minimum]-1] = obj # O(k)
        position[key(obj)-minimum] += 1 # O(k)
    return output[::-1] if reverse else output # O(N) / O(1)

def get_digit(num: int, digit: int) -> int:
    """
    Gets a specific digit of an integer (0 is the rightmost digit).
    - Input:
            - num (int): The number to find the digit of.
            - digit (int): The specific digit to find.
    - Returns (int): The digit. 
    - Time Complexity: O(1).
    - Aux space complexity: O(1).
    """
    if digit < 0:
        raise ValueError('Digit must be greater than 0')
    return num // 10**digit % 10

def radix_sort(lst: 'list[Any]', key: Callable[[Any], int] = default_key, reverse: bool = False) -> 'list[Any]':
    """
    Radix sort implementation.
    - Input:
            - lst (list[Any]): The list to be sorted.
            - key (Callable[[Any], int], optional): Function to map the list objects to an integer value. Defaults to default_key.
            - reverse (bool, optional): Whether or not the list should be in non-increasing order. Defaults to False (non-decreasing).
    - Returns (list[Any]): The sorted list. 
    - Time Complexity: O((N+b) * k * p), where N == len(lst), b = base of integers, k = O(key) and p is the amount of digits.
    - Aux space complexity: O(N), as in counting sorts O(N+u), u == N in radix sort.
    """
    max_int = key(max(lst, key=key)) # O(N*k)
    max_digits = len(str(max_int)) # O(1)
    new_lst = [i for i in lst] # O(N)
    for d in range(max_digits): # O((N+b) * k * p)
        new_lst = counting_sort(new_lst, key=lambda n: get_digit(key(n), d)) # O(N*k)
    return new_lst[::-1] if reverse else new_lst # O(N) / O(1)

def hash_uppercase_string(string: str, base: int) -> int:
    """
    Hashes an uppercase string into an integer in a certain base.
    - Input:
            - string (str): The string to hash.
            - base (int): The base the integer will be represented in.
    - Returns (int): The integer representing the uppercase string. 
    - Time Complexity: O(M) where M is the length of the string.
    - Aux space complexity: O(1).
    """
    val: int = 0 # O(1)
    for i in range(len(string)): # O(M)
        c = string[len(string)-1-i] # get i'th element (from the right) O(1)
        val += (ord(c) - ord('A') + 1) * base**i # add to val O(1)
    return val

def unique_sorted_list(lst: 'list[Any]') -> 'list[Any]':
    """
    Creates a unique list from a sorted one.
    - Input:
            - lst (list[Any]): The sorted list.
    - Returns (list[Any]): A new list with all duplicates removed. 
    - Time Complexity: O(N*c), where N is the length of lst and c is the cost of comparison.
    - Aux space complexity: O(N).
    """
    unique_results: 'list[Any]' = [lst[0]] # initialise unique array O(1)
    for i in range(1, len(lst)): # fill unique array O(N*c)
        if lst[i] != lst[i-1]: # check if duplicate match exists, O(c)
            unique_results.append(lst[i]) # if matches are not duplicate append to unique array O(1)
    return unique_results

def get_top_results(lst: 'list[Any]', k: int, start: int = 0, stop: int = None) -> 'list[Any]':
    """
    Gets the top k results from a descending sorted list.
    - Input:
            - lst (list[Any]): Sorted list.
            - k (int): The amount of top elements to find.
            - start (int, optional): The index to start at (inclusive). Defaults to 0, if start given but no stop, stop == start.
            - end (int, optional): The index to finish looking (non inclusive). Defaults to len(lst).
    - Returns (list[Any]): The top elements. 
    - Time Complexity: O(k) where k is the amount of results to return.
    - Aux space complexity: O(k).
    """
    i = 0 if stop is None else start # O(1)
    stop = stop or start or len(lst) # O(1)
    topResults: 'list[Any]' = [] # initialise top10 O(1)
    while i < stop and len(topResults) < k: # fill top10 array O(k) 
        topResults.append(lst[i]) # O(1)
        i += 1 # O(1)
    return topResults

def find_matches(lst: 'list[Any]', e: int, key: Callable[[Any], int] = default_key) ->  'list[Any]':
    """
    Creates a sublist of a non-increasing list that are equal to an integer value (or closest larger if no exact matches are found).
    - Input:
            - lst (list[Any]): The list to find the matches, list must be sorted in non-increasing order based on the value that key will map to.
            - e (int): The integer value to match to.
            - key (Callable[[Any], int], optional): Function to map an object in lst to an integer to compare with e. Defaults to default_key.
    - Returns (list[Any]): A sublist of lst that has all matches (or closest above) to the integer value e. 
    - Time Complexity: O(N*k), where N == len(lst) and k is the complexity of the key function.
    - Aux space complexity: O(N).
    """
    searchedmatches: 'list[Any]' = [] # initialise matches array O(1)
    for i, current_match in enumerate(lst): # iterate over results O(N*k)
        if key(current_match) >= e: # check if the score of current match is at least score O(k)
            if not len(searchedmatches):
                searchedmatches.append(current_match) # if empty add first O(1)
            else:
                previous_match = lst[i-1] # otherwise get previous result O(1)
                if key(current_match) - e < key(previous_match) - e: # if the current difference is less than previous O(k)
                    searchedmatches = [current_match] # replace array with just the current match O(1)
                elif key(current_match) - e == key(previous_match) - e: # if current difference is the same O(k)
                    searchedmatches.append(current_match) # add current match to array
    return searchedmatches

def analyze(results:'list[list]', roster: int, score: int) -> 'list[list]':
    """
    Analyzes tournament results. First creates a list of all results, doubling the amount of results as it includes results from both teams in a given match. 
    Then sorting is done on results, duplicates are removed and the top10 and matched results are found.
    - Input:
            - results (list[list]): The tournament's results, where each result is in format [team1, team2, score].
            - roster (int): The length of the character set that makes up team names.
            - score (int): The score (0-100) that team1 scored against team2 or 100-score that team2 scored against team1.
    - Returns (list[list]): A list including the top 10 matches in terms of score, sorted by score, team1 then team2 and a list of matches (or close matches) to the searched score parameter. 
    - Time Complexity: O(N*M). Due to roster being regarded as constant, radix sort becomes O(N*k), where N is the length of the list and k is the complexity of the key function. 
    This is because the base of the numbers is constant, and the amount of digits is equal to roof(log10(roster)) which would be considered a constant.
    - Aux space complexity: O(N*M).
    """    
    all_results: list[list] = [] # create empty list to store all results (both teams score) O(1)
    for match in results: # O(N*M)
        team1, team2, score_match = match # O(1)
        team1 = ''.join(radix_sort(team1, lambda c: ord(c) - ord('A'))) # sort team1 names O(M)
        team2 = ''.join(radix_sort(team2, lambda c: ord(c) - ord('A'))) # sort team2 names O(M)
        all_results.append([team1, team2, score_match]) # O(1)
        all_results.append([team2, team1, 100-score_match]) # O(1)

    all_results = radix_sort(all_results, lambda match: hash_uppercase_string(match[1], roster)) # sort by team2 O(N*M)
    all_results = radix_sort(all_results, lambda match: hash_uppercase_string(match[0], roster), True) # sort by team1 O(N*M)
    all_results = radix_sort(all_results, lambda match: match[2], True) # sort by score O(N)
    
    unique_results = unique_sorted_list(all_results) # O(N) as cost of comparison is constant
    top10matches = get_top_results(unique_results, 10) # O(1) as 10 is constant
    searchedmatches = find_matches(unique_results, score, lambda match: match[2]) # O(N) as key complexity is O(1).
    return [top10matches, searchedmatches]
