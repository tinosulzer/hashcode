"""Class for reading in and storing problem specification.

R (1 ≤ R ≤ 1000) d enotes the number of rows in the data center,
S (1 ≤ S ≤ 1000) denotes the number of slots in each row of the data center,
U (0 ≤ U ≤ R × S) denotes the number of unavailable slots,
P (1 ≤ P ≤ 1000) denotes the number of pools to be created,
M (1 ≤ M ≤ R × S) denotes the number of servers to be allocated;

U subsequent lines describing the unavailable slots of the data center.
M subsequent lines describing the servers to be allocated."""

class Problem:
    def __init__(self, filename):
        with open(filename) as f:
            line = f.readline()
            field = [int(i) for i in line.split()]
            self.R = field[0] # Rows
            self.S = field[1] # Slots per row
            self.U = field[2] # Unavailable slots
            self.P = field[3] # Pools to be created
            self.M = field[4] # Number of servers to allocate
            self.available = {} # Availability of slots
            for i in range(self.R):
                for j in range(self.S):
                    self.available[(i, j)] = True
            for _ in range(self.U):
                line = f.readline()
                coords = tuple(int(i) for i in line.split())
                self.available[coords] = False
            self.sizes = {} # Server size
            self.capacities = {} # Server capacity
            self.caps_to_sizes = {} # Server capacity per size
            for i in range(self.M):
                line = f.readline()
                size, capacity = [int(j) for j in line.split()]
                self.sizes[i] = size
                self.capacities[i] = capacity
                self.caps_to_sizes[i] = capacity/size
        assert len(self.available) == self.R*self.S
        assert len([k for k, v in self.available.items() if not v]) == self.U
        assert len(self.sizes) == self.M
        assert len(self.capacities) == self.M

if __name__ == "__main__":
    test = Problem("../../inputs/test.in")
    print(test.R)
    print(test.S)
    print(test.U)
    print(test.P)
    print(test.M)
    prob = Problem("../../inputs/dc.in")
    print(prob.R)
    print(prob.S)
    print(prob.U)
    print(prob.P)
    print(prob.M)
