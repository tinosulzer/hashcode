"""Dynamic programming approach

(Haven't actually added the dynamic programming yet)"""
from utils.reader import Problem
from utils.solution import Solution
from random import randint, choice

def find_row_segments(problem):
    """Returns array of continuous spaces in each row"""
    [[]*problem.R]


if __name__ == "__main__":
    problem = Problem("../inputs/dc.in")
    solution = Solution(problem)
    # Split into 2 parts:
    # Randomly allocate servers ordered by capacity per size
    M, P = problem.M, problem.P
    loc = (0, 0)
    servers = list(range(M))
    servers.sort(key = lambda x: problem.capacities[x])
    s = servers.pop(0)
    while s < M:
        p = randint(0, P-1)
        if solution.add_server(s, loc, p):
            s = servers.pop(0)
        else:
            loc = (loc[0], loc[1] + 1)
            if loc[1] >= problem.S:
                loc = (loc[0]+1, 0)
            if loc[0] >= problem.R:
                print(loc[0])
                break
    # Then maximimise garanteed capacity of each pool
    # Consider each pair of servers in order
    # see if swapping pools would improve score
    for s, p in solution.pools.items():
        score = solution.score()
        print(s)
        print(solution.score())
        for s2, p2 in solution.pools.items():
            if s2 > s and p2 != p:
                solution.pools[s] = p2
                solution.pools[s2] = p
                if solution.score() > score:
                    score = solution.score()
                    break
                else:
                    solution.pools[s] = p
                    solution.pools[s2] = p2
    print(solution.score())
    solution.print_solution("../outputs/dp.txt")
