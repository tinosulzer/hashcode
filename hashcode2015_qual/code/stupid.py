"""Really stupid solution, allocate randomly"""
from utils.reader import Problem
from utils.solution import Solution
from random import randint, choice

if __name__ == "__main__":
    problem = Problem("../inputs/dc.in")
    solution = Solution(problem)
    M, P = problem.M, problem.P
    loc = (0, 0)
    s = 0
    while s < M:
        p = randint(0, P-1)
        if solution.add_server(s, loc, p):
            s += 1
        else:
            loc = (loc[0], loc[1] + 1)
            if loc[1] >= problem.S:
                loc = (loc[0]+1, 0)
            if loc[0] >= problem.R:
                print(loc[0])
                break
    print(solution.score())
    solution.print_solution("../outputs/stupid.txt")
