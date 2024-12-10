
import random, time
from solver import _Solver
from solvers.localSearch import LocalSearch

class Solver_Greedy(_Solver):
    
    def _selectCandidate(self, teachers):
        if self.config.solver == 'Greedy':
            # sort candidate assignments by highestLoad in ascending order
            sortedTeachersList = sorted(teachers, key=lambda m: sum(m.compatibility.values()), reverse=True)
            # choose assignment with minimum highest load
            return sortedTeachersList[0]
        return random.choice(teachers)

    def construction(self):
        # get an empty solution for the problem
        solution = self.instance.createSolution()
        sizeCommittee = self.instance.getSizeCommittee()
        # for each task taken in sorted order
        for i in range(0, sizeCommittee):
            # compute feasible assignments
            candidateList = solution.getFeasibleTeachers()
            # no candidate assignments => no feasible assignment found
            if not candidateList:
                solution.makeInfeasible()
                break
            # select assignment
            candidate = self._selectCandidate(candidateList)
            # assign the current task to the CPU that resulted in a minimum highest load
            solution.assign(candidate)
    
        return solution

    def solve(self, **kwargs):
        self.startTimeMeasure()

        solver = kwargs.get('solver', None)
        if solver is not None:
            self.config.solver = solver
        localSearch = kwargs.get('localSearch', None)
        if localSearch is not None:
            self.config.localSearch = localSearch

        self.writeLogLine(float('inf'), 0)

        solution = self.construction()
        if self.config.localSearch:
            localSearch = LocalSearch(self.config, None)
            endTime= self.startTime + self.config.maxExecTime
            solution = localSearch.solve(solution=solution, startTime=self.startTime, endTime=endTime)

        self.elapsedEvalTime = time.time() - self.startTime
        self.writeLogLine(solution.getFitness(), 1)
        self.numSolutionsConstructed = 1
        self.printPerformance()
        if solution.enforce_high_compatibility_condition():
            solution.makeInfeasible()
        return solution