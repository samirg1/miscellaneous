# Solver for the word game from the popular Countdown TV show game.
# Date: 10-11-2022
# Author: Samir Gupta

from enchant import Dict  # type: ignore

d = Dict('en_US')
TOTAL_LETTERS = 9


def word_game():
    """
    Solves the Countdown word game.
    - Time Complexity: O(n! * c), where n is the length of the word and c is the complexity of the dictionary check function..
    - Aux space complexity: O(n!).
    """
    letters = ''
    while len(letters) != TOTAL_LETTERS or not letters.isalpha():
        letters = input('Enter 9 letters below: ')
    letters_list = [c.lower() for c in letters]

    for n in range(TOTAL_LETTERS, 0, -1):
        possibles: set[str] = set(get_word(letters_list, n))
        if possibles:
            return print(f'Max Length: {n}\n{list(possibles)}\nTotal: {len(possibles)}')


def get_word(letters: list[str], n: int, part: str = '') -> list[str]:
    """
    Gets all possible valid English words of length n, that contain the letters in the list.
    - Input:
        - letters (list[str]): The list of possible letters the word can contain.
        - n (int): The length of the word.
        - part (str, optional): The partial solution. Defaults to ''.
    - Returns (list[str]): List of possible words of length n. 
    - Time Complexity: O(n! * c), where n is the length of the word and c is the complexity of the dictionary check function.
    - Aux space complexity: O(n!).
    """
    if len(part) == n:
        if d.check(part):  # type: ignore
            return [part]
        return []
    else:
        res: list[str] = []
        for o in letters:
            aug = part + o
            p = [l for l in letters]
            p.remove(o)
            res += get_word(p, n, aug)
        return res


def main():
    word_game()


if __name__ == '__main__':
    main()
