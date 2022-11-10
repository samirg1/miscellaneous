# Exam calculator to calculate what marks get what total score for a uni subject.
# Date: 10-11-2022
# Author: Samir Gupta


from typing import NamedTuple


class Result(NamedTuple):
    """
    Named tuple for a result.
    """

    score: float
    total: int


class Subject:
    """
    Class representing a subject.
    """

    def __init__(self, name: str, results: list[Result] | None = None):
        """
        Initialise the subject.
        - Input:
            - name (str): The name of the subject.
            - results (list[Result] | None, optional): List of results for the subject. Defaults to None.
        - Time Complexity: O(1).
        - Aux space complexity: O(n), where n is the amount of results.
        """
        self._name = name
        self._results = results if results is not None else []

    @property
    def _score(self) -> float:
        """
        Returns the total current score.
        - Returns (float): The total current score.
        - Time Complexity: O(n), where n is the amount of results.
        - Aux space complexity: O(1).
        """
        return sum(res.score for res in self._results)

    @property
    def _total(self) -> int:
        """
        Return the total amount of marks that were available.
        - Returns (int): The total amount of marks.
        - Time Complexity: O(n), where n is the amount of results.
        - Aux space complexity: O(1).
        """
        return sum(res.total for res in self._results)

    def get_percentage(self, n: int) -> float:
        """
        Get the percentage needed for a particular overall score.
        - Input:
            - n (int): The overall score desired.
        - Returns (float): The percentage needed to get the score.
        - Time Complexity: O(n), where n is the amount of results.
        - Aux space complexity: O(1).
        """
        return round((n - self._score) * 100 / (100 - self._total), 1)

    def __repr__(self) -> str:
        """
        Represent the subject as a string.
        - Returns (str): The string representation.
        - Time Complexity: O(n), where n is the amount of results.
        - Aux space complexity: O(1).
        """
        return f'{self._name} : {round(self._score, 1)} / {self._total}'


def main():
    subjects = [
        Subject('FIT3171', [Result(50.93, 60)]),
        Subject('FIT2107', [Result(27 / 35 * 20, 20), Result(15.5, 25), Result(26.5 / 35 * 15, 15)]),
        Subject('FIT2004', [Result(8.5, 10), Result(16, 20), Result(17, 20)]),
        Subject('FIT2101', [Result(14.1, 15), Result(7.85, 10), Result(8.7, 10), Result(12.9, 15), Result(7.8, 10)]),
    ]

    for subject in subjects:
        print(f'\n{subject}')
        for final_score in range(70, 105, 5):
            percentage = subject.get_percentage(final_score)
            if percentage <= 100:
                print(f'{final_score} = {percentage}%')


if __name__ == '__main__':
    main()
