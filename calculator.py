# Calculator for basic operations using divide and conquer without using exec, eval etc.
# Date: 10-11-2022
# Author: Samir Gupta


from typing import Union

class Equation():
    """
    Class to represent an equation to solve
    """
    numbers = [str(n) for n in range(10)] + ['.'] # valid numbers a decimal point
    brackets = ['(', ')'] # bracket symbols
    symbols = ['-', '+', '/', '*', '^'] # valid operational symbols

    def __init__(self, raw_eq: str, initial: bool=False) -> None:
        """
        Constructor.

        Args:   
            raw_eq (str): The raw equation to solve.
            initial (bool, optional): Whether or not this is the initial equation. Defaults to `False`.

        Complexity:
            If initial: O(v), where v is the complexity of the `validate` method.
            otherwise: O(1).
        """
        self.pairs: int = 0
        self.eq = raw_eq
        if initial:
            self.eq = ''.join([c for c in raw_eq if c != ' ']) # clear whitespace O(l)
            self.__validate() # validate equation O(l*m)
    
    def __validate(self) -> None:
        """
        Validates the equation.

        Raises:
            ValueError: If the raw equation is invalid.
        
        Complexity:
            O(l*m), where l is the length of the equation and m is the amount of negatives in the equation.
        """
        i = self.eq.find('(-') # find any negatives O(l)
        while i != -1: # loop to remove all negatives O(l*m)
            j = self.eq.find(')', i) # find the closing bracket O(l)
            self.eq = self.eq[:i] + '0-' + self.eq[j-1] + self.eq[j+1:] # replace the negative O(l)
            i = self.eq.find('(-') # find any more negatives O(l)

        for i in range(len(self.eq)): # validate equation O(l)
            if self.eq[i] not in (self.numbers + self.brackets + self.symbols): # find invalid characters O(1)
                raise ValueError(f"Invalid character '{self.eq[i]}'")
            if not i and self.eq[i] not in self.numbers + self.brackets[:1]: # find invalid starting characters O(1)
                raise ValueError(f"Invalid starting character '{self.eq[i]}'")
            if i and self.eq[i-1] in self.symbols + self.brackets[:1] and self.eq[i] in self.symbols + self.brackets[1:]: # find invalid character pairs O(1)
                raise ValueError(f"Invalid syntax '{self.eq[i-1]}{self.eq[i]}'")
        
        
        op, cl = self.eq.count('('), self.eq.count(')') # get counts of brackets O(l)
        if op != cl: # validate amount of closing vs opening brackets O(1)
            raise ValueError(f'Invalid syntax - not all brackets are closed')
        self.pairs = op

    def __find_pair(self) -> "tuple[int, int]":
        """
        Find the next pair of brackets.

        Returns:
            tuple[int, int]: First element is the index of the opening bracket and the second is the index of the closing bracket.

        Complexity:
            O(l), where l is the length of the equation.
        """
        lo = self.eq.rfind('(') # O(l)
        hi = self.eq.find(')', lo) # O(l)
        return (lo, hi) 
        
    def __solve_basic(self, symbol: str) -> Union[float, int]:
        """
        Solve an equation with one type of symbol.

        Args:
            symbol (str): The symbol in the equation.

        Returns:
            (float | int): The solution to the equation.

        Complexity:
            O(l + c*s), where l is the length of the equation, c symbol count and s is the complexity of the `solve` function.
        """
        lst = self.eq.split(symbol) # split the equation by the symbol O(l)
        res = Equation(lst[0]).solve() # solve the first part of the equation O(s)
        for eq in lst[1:]: # solve all of the other parts of the equation O(c*s)
            next_val = Equation(eq).solve() # get the next value O(s)
            if symbol == '+':
                res += next_val
            elif symbol == '-':
                res -= next_val
            elif symbol == '*':
                res *= next_val
            elif symbol == '/':
                res /= next_val
            elif symbol == '^':
                res = res ** next_val
        return res

    def solve(self) -> Union[float, int]:
        """
        Solve the equation.

        Returns:
            (float | int): The solution to the equation.

        Complexity:
            O(l*(c+p)), where l is the length of the equation, c is the amount of symbols, and p is the amount of bracket pairs.
        """
        for _ in range(self.pairs): # go through and solve all bracket pairs O(p * s)
            lo, hi = self.__find_pair() # find the bracket pair O(l)
            value = Equation(self.eq[lo+1:hi]).solve() # solve the pair O(s)
            self.eq = self.eq[:lo] + str(value) + self.eq[hi+1:] # replace the pair O(l)
        
        for symbol in self.symbols: # solve the equation by symbol O(b)
            if symbol in self.eq:
                return self.__solve_basic(symbol) # O(b)

        return float(self.eq) if float(self.eq) % 1 else int(self.eq) # return solution O(1)

equation = Equation('1+(-3)*4', True)
print(equation.solve())

"""
Equation.solve complexity analysis.
From function:
    O(p * s + b), where p is the amount of pairs, s is the complexity of the solve method, and b is the complexity of the `solve_basic` function.
    = O(p * s + l + c * s)
    = O(l + (c+p)*s)
    Since the input size is in worst case descreasing by 2 each iteration, O(s) is in O(l).
    O(l + (c+p)*l)
    = O(l(c+p))
"""