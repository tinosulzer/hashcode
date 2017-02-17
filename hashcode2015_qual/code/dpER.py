"""Dynamic programming approach

(Haven't actually added the dynamic programming yet)"""
from utils.reader import Problem
from utils.solution import Solution, check_solution_file
from random import randint, choice

def find_row_segments(problem):
    """Returns array of continuous spaces in each row"""
    [[]*problem.R]


if __name__ == "__main__":
    problem = Problem("../inputs/dc.in")
    solution = Solution(problem)
    # Split into 3 parts:
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
    # For each server, try reallocating to a different pool and keep if the score is increased. Keep looping over until the score is not increased.
    old_score = solution.score()-1
    score = solution.score()
    while old_score!=score:
        old_score=solution.score()
        for s, p_old in solution.pools.items():
            new_p=p_old
            for p_test in range(problem.P):
                solution.pools[s]=p_test
                score_test = solution.score()
                if score_test>score:
                    new_p = p_test
                    score = score_test
            solution.pools[s]=new_p
            print(s,score)

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
    solution.print_solution("../outputs/dpER.txt")
    check_solution_file(problem, "../outputs/dpER.txt")
