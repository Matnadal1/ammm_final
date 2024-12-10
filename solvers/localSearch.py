import copy
import time
from solver import _Solver
from AMMMGlobals import AMMMException

# Implementation of a local search using an exchange neighborhood.
class LocalSearch(_Solver):
    def __init__(self, config, instance):
        self.enabled = config.localSearch
        self.policy = config.policy
        self.maxExecTime = config.maxExecTime
        super().__init__(config, instance)

    def exploreExchange(self, solution):
        neighbor = None
        _, current_fitness = solution.calculate_compatibility_metrics()
        nonAssignedTeachers = [teacher for teacher in solution.teachers if teacher.idN not in [t.idN for t in solution.committee]]

        for committeeTeacher in solution.committee:
            neighborSolution = copy.deepcopy(solution)
            neighborSolution.unassign(committeeTeacher)
            for nonAssignedTeacher in nonAssignedTeachers:
                if not neighborSolution.assign(nonAssignedTeacher):
                    continue

                _, neighbor_fitness = neighborSolution.calculate_compatibility_metrics()
                
                if neighbor_fitness > current_fitness:
                    neighbor = neighborSolution
                    current_fitness = neighbor_fitness
                    if self.policy == "BestImprovement":
                        continue
                    elif self.policy == "FirstImprovement" :
                        return neighbor

        return neighbor

    def solve(self, **kwargs):
        initialSolution = kwargs.get('solution', None)
        if initialSolution is None:
            raise AMMMException('[local search] No solution could be retrieved')

        if not initialSolution.isFeasible():
            return initialSolution

        self.startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)

        incumbent = initialSolution
        _, _ = incumbent.calculate_compatibility_metrics()
        iterations = 0

        # Log the start of the local search
        #print(f"Starting local search with max execution time: {self.maxExecTime}s")
        #print(f"Initial solution fitness: {incumbent.fitness}")
        #print(f"Initial committee: {[teacher.idN for teacher in incumbent.committee]}")

        # Keep iterating while improvements are found until convergence or time runs out
        while time.time() < endTime:
            iterations += 1
           # print(f"\nIteration {iterations}: Current fitness: {incumbent.fitness}")
            neighbor = self.exploreExchange(incumbent)
            
            if neighbor is None:
                #print("No better neighbor found. Convergence achieved.")
                break

            incumbent = neighbor

        # Log the end of the local search
        #print(f"\nLocal search finished after {iterations} iterations.")
        #print(f"Final solution fitness: {incumbent.fitness}")
        #print(f"Final committee: {[teacher.idN for teacher in incumbent.committee]}")

        return incumbent
