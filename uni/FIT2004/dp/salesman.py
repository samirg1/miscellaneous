from typing import cast


def salesman_up(houses: list[int]) -> int:
    memo = [0 for _ in houses] 
    memo[0] = houses[0]
    memo[1] = max(houses[0], houses[1])
    
    for i in range(2, len(houses)):
        memo[i] = max(houses[i] + memo[i-2], memo[i-1])

    return memo[len(houses)-1]

def salesman_down(houses: list[int]) -> int:
    memo: list[int|None] = [None for _ in houses]
    
    def salesman_down_aux(houses: list[int], n: int = None) -> int:
        n = len(houses) - 1 if n is None else n
        if n == 1:
            return houses[n-1]
        elif n == 2:
            return max(houses[n-1], houses[n-2])

        if memo[n] is None:
            profit = max(salesman_down_aux(houses, n-1), salesman_down_aux(houses, n-2) + houses[n])
            memo[n] = profit
            return profit

        return cast(int, memo[n])

    return salesman_down_aux(houses)

def main():
    houses = [50, 10, 12, 65, 40, 95, 100, 12, 20, 30]
    profit_up = salesman_up(houses)
    profit_down = salesman_down(houses)
    print(f'{profit_up = }\n{profit_down = }')

if __name__ == '__main__':
    main()