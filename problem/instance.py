from problem.Teacher import Teacher
from problem.solution import Solution

class Instance(object):
    def __init__(self, config, inputData):
        self.config = config
        self.inputData = inputData
        D = inputData.D
        N = inputData.N
        inputData.n = list(inputData.n)
        n = inputData.n
        inputData.d = list(inputData.d)
        d = inputData.d
        inputData.m = list(inputData.m)
        m = inputData.m
        self.compatibility = []
        for row in m:
            row = list(row)
            self.compatibility.append(row)
        self.teachers = []
        self.departments = {i + 1: n[i] for i in range(D)}
        to_dict = lambda l: {i + 1: l[i] for i in range(len(l))}
        for i in range(N):
            department = d[i]
            compatibility = to_dict(self.compatibility[i])
            self.teachers.append(Teacher(i + 1, department, compatibility))
            
    def getNumTeachers(self):
        return len(self.teachers)
    
    def getTeachers(self):
        return self.teachers
    
    def getSizeCommittee(self):
        return sum(self.departments.values())
    
    def getDepartments(self):
        return self.departments
        
    def getCompatibility(self):
        return self.compatibility

    def createSolution(self):
        solution = Solution(self.departments, self.teachers, self.compatibility)
        solution.setVerbose(self.config.verbose)
        return solution

    def checkInstance(self):
        return True
"""
    def checkInstance(self):
        totalCapacityCPUs = 0.0
        maxCPUCapacity = 0.0
        for cpu in self.cpus:
            capacity = cpu.getTotalCapacity()
            totalCapacityCPUs += capacity
            maxCPUCapacity = max(maxCPUCapacity, capacity)

        totalResourcesTasks = 0.0
        for task in self.tasks:
            resources = task.getTotalResources()
            totalResourcesTasks += resources
            if resources > maxCPUCapacity: return False

        return totalCapacityCPUs >= totalResourcesTasks
"""