# **Committee Formation with Compatibility Optimization**

This project implements heuristics-based approaches (Greedy, GRASP, Local Search) for solving the problem of forming committees of teachers with the highest possible compatibility. The objective is to ensure committees have representatives from departments while maximizing compatibility between members.

---

## **Table of Contents**
1. [Project Structure](#project-structure)
2. [How It Works](#how-it-works)
3. [Usage](#usage)
4. [Example Input File](#example-input-file)
5. [Features](#features)
6. [Future Enhancements](#future-enhancements)
7. [Dependencies](#dependencies)
8. [Contributors](#contributors)
9. [License](#license)

---

## **Project Structure**

### **Main Modules**

1. **`Main.py`**
   - The entry point for the application.
   - Processes input data files, runs the specified heuristic solver, and logs solutions into a global CSV (`solutions.csv`).

2. **`solver_Greedy.py`**
   - Implements the Greedy solver.
   - Selects candidates with the highest cumulative compatibility values iteratively.

3. **`solver_GRASP.py`**
   - Implements the GRASP (*Greedy Randomized Adaptive Search Procedure*) solver.
   - Combines greedy selection with randomization for diverse solution exploration.

4. **`localSearch.py`**
   - Implements local search to refine solutions using neighborhood exploration (e.g., exchange of committee members).

5. **`instance.py`**
   - Defines the problem instance and initializes data structures (teachers, departments, and compatibility matrix).

6. **`solution.py`**
   - Manages solutions, including feasibility checks, compatibility calculations, and saving results in a structured CSV format.

7. **`Teacher.py`**
   - Defines the `Teacher` class, representing committee members and their compatibility relationships.

---

## **How It Works**

### **Problem Description**
The problem involves:
- Selecting committee members from a pool of teachers.
- Ensuring department representation constraints are satisfied.
- Maximizing compatibility among committee members.

### **Input**
Each input file contains:
- Number of departments (`D`).
- Number of representatives needed per department (`n`).
- Total number of teachers (`N`).
- Teachers' department affiliations (`d`).
- Compatibility matrix (`m`).

### **Output**
The output is written to `solutions.csv` with:
- Problem parameters (`D`, `N`, `n`, `d`).
- Total and mean compatibility of the committee.
- Committee structure (teacher IDs and their department).
- Solver details (`heuristic_name`, `localsearch`, `policy`).
- Performance metrics (`nb_of_iteration`, `elapsed_time`).

---

## **Usage**

### **Running the Program**
1. **Prepare Input Data:**
   - Place input files in a directory and configure the `config.dat` file to point to this directory.
2. **Run the Program:**
   ```bash
   python Main.py -c path/to/config.dat
   ```

### **Configuration**
Set the parameters in `config.dat`:
```plaintext
# --- Common Parameters ---
inputDataFile        = output;              # Directory for input data files
solutionFile         = solutions;           # Directory for solutions
solver               = GRASP;               # Solver: Greedy / GRASP
maxExecTime          = 30;                  # Maximum execution time in seconds
verbose              = True;                # Enable verbose output

# --- GRASP Parameters ---
alpha                = 0.7;                 # Randomization factor for GRASP

# --- Local Search Parameters ---
localSearch          = True;                # Enable local search
neighborhoodStrategy = Reassignment;        # Neighborhood strategy: Exchange or Reassignment
policy               = FirstImprovement;    # Search policy: FirstImprovement or BestImprovement
```

---

## **Example Input File**

Below is an example of an input file used for the committee formation problem:

```plaintext
D=2;
n=[4 1];
N=10;
d=[1 1 1 2 1 2 1 2 2 1];
m = [
  [1.00 0.55 0.92 0.90 0.24 0.99 0.12 0.04 0.52 0.68]
  [0.55 1.00 0.15 0.59 0.86 0.32 0.57 0.72 0.88 0.12]
  [0.92 0.15 1.00 0.24 0.91 0.22 0.26 0.59 0.91 0.18]
  [0.90 0.59 0.24 1.00 0.20 0.27 0.70 0.87 0.22 0.36]
  [0.24 0.86 0.91 0.20 1.00 0.79 0.09 0.19 0.52 0.18]
  [0.99 0.32 0.22 0.27 0.79 1.00 0.15 0.25 0.98 0.61]
  [0.12 0.57 0.26 0.70 0.09 0.15 1.00 0.93 0.28 0.75]
  [0.04 0.72 0.59 0.87 0.19 0.25 0.93 1.00 0.95 0.35]
  [0.52 0.88 0.91 0.22 0.52 0.98 0.28 0.95 1.00 0.21]
  [0.68 0.12 0.18 0.36 0.18 0.61 0.75 0.35 0.21 1.00]
];
```

This input specifies:
- The number of departments (`D=2`).
- The number of representatives required per department (`n=[4 1]`).
- The total number of teachers (`N=10`).
- Each teacher's department (`d=[1 1 1 2 1 2 1 2 2 1]`).
- A compatibility matrix (`m`), where `m[i][j]` is the compatibility score between teacher `i` and teacher `j`.

To use this file:
1. Save the content in a `.dat` file (e.g., `project10_1.dat`).
2. Place it in the directory specified in your `config.dat` under `inputDataFile`.
3. Run the program, and the solver will process this input.

---

## **Features**

1. **Multiple Heuristics:**
   - Greedy: Deterministic and fast.
   - GRASP: Combines greedy and randomized exploration.

2. **Local Search Refinement:**
   - Enhances solutions by swapping committee members to improve compatibility.

3. **Robust Metrics Tracking:**
   - Captures iterations, runtime, and compatibility metrics.

4. **Comprehensive Logging:**
   - Outputs solutions and performance metrics to a CSV.

---

## **Dependencies**
- Python 3.8+
- No external libraries required (standard Python library).

---

## **Contributors**
- **Author:** Luis Velasco  
- **Maintainer:** Matthias NADAL | Virginia NICOSIA

---

## **License**
This project is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html).
