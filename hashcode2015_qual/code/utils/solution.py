"""Class for storing solution to problem."""
from .reader import Problem

class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.locations = {}
        self.pools = {}
        self.rows = {}
        self.pool_caps = {pool: 0 for pool in range(self.problem.P)} # Capacity for each pool
        self.unallocated = list(range(self.problem.M))
        self.available_slots = problem.available.copy()
        for r in range(self.problem.R): # Tuple of capacity and free space for each row
            self.rows[r] = (0,sum([self.available_slots[(r,slot)] for slot in range(self.problem.S)]))

    def add_server(self, s, loc, p):
        """Adds server s to location loc and pool p."""
        if not self.problem.available[loc]:
            print("Trying to allocate server to unavailable slot.")
            return False
        elif p >= self.problem.P:
            print("Trying to allocate server to non-existent pool")
        elif (s not in self.unallocated) or (s in self.locations) or (s in self.pools):
            print("Server already allocated")
            return False
        for i in range(self.problem.sizes[s]):
            if loc[1] + i >= self.problem.S:
                print("Server extends past end of row.")
                return False
            elif not self.available_slots[(loc[0], loc[1] + i)]:
                print("Slot occupied by other server")
                return False
        for i in range(self.problem.sizes[s]):
            self.available_slots[(loc[0], loc[1] + i)] = False
        self.locations[s] = loc
        self.pools[s] = p
        # Update row capacity
        self.rows[loc[0]][0] += self.problem.capacities[s]
        # Update row free spaces
        self.rows[loc[0]][1] -= self.problem.sizes[s]
        # Update pool capacity
        self.pool_caps[p] += self.problem.capacities[s]
        self.unallocated.remove(s)
        return True

    def remove_server(self, s):
        """Remove server s from allocated slot and pool."""
        if (s in self.unallocated) or (s not in self.locations) or (s not in self.pools):
            print("Server not currently allocated.")
            return False
        loc = self.locations.pop(s)
        for i in range(self.problem.sizes[s]):
            self.available_slots[(loc[0], loc[1] + i)] = True
        del self.pools[s]
        self.unallocated.append(s)
        return True

    def add_server_loc(self, s, loc):
        """Adds server s to location loc without assigning pool."""
        if not self.problem.available[loc]:
            print("Trying to allocate server to unavailable slot.")
            return False
        elif (s not in self.unallocated) or (s in self.locations) or (s in self.pools):
            print("Server already allocated")
            return False
        for i in range(self.problem.sizes[s]):
            if loc[1] + i >= self.problem.S:
                print("Server extends past end of row.")
                return False
            elif not self.available_slots[(loc[0], loc[1] + i)]:
                print("Slot occupied by other server")
                return False
        for i in range(self.problem.sizes[s]):
            self.available_slots[(loc[0], loc[1] + i)] = False
        self.locations[s] = loc
        # Update row capacity
        self.rows[loc[0]][0] += self.problem.capacities[s]
        # Update row free spaces
        self.rows[loc[0]][1] -= self.problem.sizes[s]
        self.unallocated.remove(s)
        return True

    def add_server_pool(self, s, p):
        """
        Adds server s to pool p.
        Server s must already have a location
        """
        if s not in self.locations.keys():
            print("Server location not yet assigned.")
            return False
        elif p >= self.problem.P:
            print("Trying to allocate server to non-existent pool")
            return False
        self.pools[s] = p
        # Update pool capacity
        self.pool_caps[p] += self.problem.capacities[s]
        return True

    def print_solution(self, filename):
        """Print solution to file."""
        with open(filename, "w") as f:
            for i in range(self.problem.M):
                if i in self.locations:
                    loc = self.locations[i]
                    p = self.pools[i]
                    f.write("{} {} {}\n".format(loc[0], loc[1], p))
                else:
                    f.write("x\n")

    def score(self):
        """Defined score"""
        pool_capac = [[0]*self.problem.R for _ in range(self.problem.P)]
        for s, loc in self.locations.items():
            p = self.pools[s]
            for j in range(self.problem.R):
                if j != loc[0]:
                    pool_capac[p][j] += self.problem.capacities[s]
        return min([min(gc) for gc in pool_capac])

    def guaranteed_capacity(self, p):
        """Returns guaranteed capacity of pool p"""
        pool_capac = [[0]*self.problem.R for _ in range(self.problem.P)]
        for s, loc in self.locations.items():
            p = self.pools[s]
            for j in range(self.problem.R):
                if j != loc[0]:
                    pool_capac[p][j] += self.problem.capacities[s]
        return min(pool_capac[p])

def check_solution_file(problem, filename):
    """Check solution file is valid"""
    M = problem.M
    R = problem.R
    S = problem.S
    slots = set((i, j) for i in range(R) for j in range(S))
    m = 0
    for k, v in problem.available.items():
        if not v:
            slots.remove(k)
    with open(filename) as f:
        for s, line in enumerate(f.readlines()):
            m += 1
            if line == "x\n":
                continue
            else:
                ar, ass, ap = [int(x) for x in line.split()]
                for j in range(problem.sizes[s]):
                    if (ar, ass+j) in slots:
                        slots.remove((ar, ass+j))
                    else:
                        print("Server {} in non-existent place.".format(s))
                        return False
                if ap >= problem.P:
                    print("Server {} in non-existent pool".format(s))
                    return False
    assert m == M
    print("File valid")
    return True


if __name__ == "__main__":
    test = Problem("../../inputs/test.in")
    solution = Solution(test)
    solution.add_server(0, (0, 1), 0)
    solution.add_server(1, (1, 0), 1)
    solution.add_server(2, (1, 3), 0)
    solution.add_server(3, (0, 4), 1)
    solution.print_solution("../../outputs/test.txt")
    print(solution.score())

    new_solution = Solution(test)
    solution.add_server(0, (0, 1), 0)
    solution.add_server(1, (1, 0), 1)
    solution.add_server(2, (1, 3), 0)
    solution.add_server_loc(3, (0, 4))
    solution.add_server_pool(3,1)
    solution.print_solution("../../outputs/test.txt")
    print(solution.score())

    check_solution_file(test, "../../outputs/test.txt")
    problem = Problem("../../inputs/dc.in")
    check_solution_file(problem, "../../outputs/stupid.txt")
    check_solution_file(problem, "../../outputs/dp.txt")
