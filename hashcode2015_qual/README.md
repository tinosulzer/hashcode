## Google HashCode 2015 Qualification round
### Optimizing a data center
---
#### Score Benchmarks
Total teams: 230

* Winner: 407
* 10th: 393
* 20th: 388
* 50th: 371
* 100th: 325

---

#### Utilities
`reader.py` class to read in problem statement

`solution.py` class to hold solution, calculate score and print to file, and a
function to check the validity of a solution.

---

#### Solution generators
`stupid.py` randomly allocate servers to spots and pools. Gets scores of ~80

`dp.py` Allocate highest capacity servers first, then see if swapping pairs will improve scores. Gets scores of ~120-140
