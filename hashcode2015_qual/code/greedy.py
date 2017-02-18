"""
Greedy Algorithm approach, first selecting the servers with biggest
capacity to size ratio and assigning to rows as cleverly as possible, then
assigning pools as uniformly as possible
"""

from utils.reader import Problem
from utils.solution import Solution
import operator
import pdb
from random import randint, choice

def getKey(item):
    return item[1]

if __name__ == "__main__":
    problem = Problem("../inputs/dc.in")
    solution = Solution(problem)
    M, P = problem.M, problem.P
    # First part: Allocate servers as uniformly as possible
        # Sort servers by size to capacity ratio
    servers = list(range(M))
    servers.sort(key = lambda x: problem.caps_to_sizes[x])
    s = servers.pop()
    #   Sort rows first by capacity then by free space
    sorted_rows = sorted(solution.rows.items(), key = operator.itemgetter(1))
    i = 0
    slot = 0
    servers_used = []
    while True:
        if solution.add_server_loc(s,(sorted_rows[i][0],slot)):
            # Add to servers used
            servers_used.append(s)
            # Reset sorting and move on to next server
            s = servers.pop()
            sorted_rows = sorted(solution.rows.items(), key = operator.itemgetter(1))
            i = 0
            slot = 0
        else:
            slot += 1
            if slot >= problem.S:
                i += 1
                slot = 0
            if i >= problem.R:
                print(i)
                break

    # Second part: Allocate pools as uniformly as possible
    #   Find pool with lowest guaranteed capacity
    #   Add biggest remaining server to that pool
    # Sort servers by capactity
    servers = list(range(M))
    servers.sort(key = lambda x: problem.capacities[x])
    # Only choose the servers that we've used (now sorted)
    servers_used = [i for i in servers if i in servers_used]
    s = servers_used.pop()
    # Calculate pool guaranteed capacities and update pool with worst one
    pool_gcs = [(p,solution.guaranteed_capacity2(p)) for p in range(P)]
    sorted_pools = sorted(pool_gcs, key = getKey)
    while True:
        if solution.add_server_pool(s,sorted_pools[0][0]):
            pool_gcs = [(p,solution.guaranteed_capacity2(p)) for p in range(P)]
            sorted_pools = sorted(pool_gcs, key = getKey)
        if not servers_used:
            break
        s = servers_used.pop()
    print(solution.score())
    solution.print_solution("../outputs/greedy.txt")
