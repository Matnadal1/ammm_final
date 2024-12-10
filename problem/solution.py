from solution import _Solution
import csv
from pathlib import Path

# Solution includes functions to manage the solution, to perform feasibility
# checks and to dump the solution into a string or file.
class Solution(_Solution):
    def __init__(self, departments, teachers, compatibility):
        self.departments = departments
        self.teachers = teachers
        self.compatibilityTable = compatibility
        self.department_representatives = {dept: 0 for dept in self.departments}
        self.totalCompatibility = []
        self.committee = []
        
        super().__init__()

    def isFeasibleToAssignTeacherToCommity(self, teacher):
        if teacher in self.committee:
            return False
        
        if self.department_representatives[teacher.department] >= self.departments[teacher.department]:
            return False
            
        if len(self.committee) > 0:
            for i, member in enumerate(self.committee):
                if teacher.compatibility[member.getId()] == 0:
                    return False
                if teacher.compatibility[member.getId()] < 0.15:
                    found = False
                    for memberk in self.committee:
                        if memberk.getId() != member.getId() and memberk.getId() != teacher.getId():
                            if (memberk.compatibility[teacher.getId()] > 0.85 and 
                                memberk.compatibility[member.getId()] > 0.85):
                                found = True
                                break
                    if not found:
                        return False
                
        return True

    def isFeasibleToUnassignTeacherFromCommity(self, teacher):
        if teacher.idN not in [t.idN for t in self.teachers]: return False
        if teacher.idN not in [c.idN for c in self.committee]: return False
        return True

    def assign(self, teacher):
        if not self.isFeasibleToAssignTeacherToCommity(teacher):return False
        teacher.selected = True
        self.department_representatives[teacher.department] += 1
        self.committee.append(teacher)
        self.updateFitness()
        return True

    def unassign(self, teacher):
        if not self.isFeasibleToUnassignTeacherFromCommity(teacher): return False
        teacher.selected = False
        self.committee = [cm for cm in self.committee if cm.idN != teacher.idN]
        self.department_representatives[teacher.department] -= 1
        self.updateFitness()
        return True

    def getFeasibleTeachers(self):
        feasibleTeachers = []
        for teacher in self.teachers:
            if teacher in self.committee:
                continue
            if self.isFeasibleToAssignTeacherToCommity(teacher):
                feasibleTeachers.append(teacher)
        return feasibleTeachers

    def updateFitness(self):
        self.fitness = 0.0
        for i in range(len(self.committee)):
            for j in range(i + 1, len(self.committee)):
                member1 = self.committee[i]
                member2 = self.committee[j]
                compatibility = member1.compatibility.get(member2.getId(), 0)
                self.fitness += compatibility


    def calculate_compatibility_metrics(self):
        total_compatibility = 0
        compatibility_list = []
        count = 0
        for i, member1 in enumerate(self.committee):
            for member2 in self.committee[i + 1:]:
                compatibility = member1.compatibility[member2.getId()]
                total_compatibility += compatibility
                compatibility_list.append(((member1.getId(), member2.getId()), compatibility))
                count += 1
        
        average_compatibility = total_compatibility / count if count > 0 else 0
        return total_compatibility, average_compatibility
    
    def enforce_high_compatibility_condition(self):
        if len(self.committee) < sum(self.departments.values()):
            self.notFeasibleReason = "Not possible to form a committee: the committee is not full"
            return False
        for i, member1 in enumerate(self.committee):
            for j, member2 in enumerate(self.committee):
                if i < j and member1.compatibility[member2.getId()] < 0.15:
                    # Check if there is a third member with high compatibility (> 0.85) with both member1 and member2
                    found = False
                    for member3 in self.teachers:
                        if member3.getId() != member1.getId() and member3.getId() != member2.getId():
                            if (member3.compatibility[member1.getId()] > 0.85 and 
                                member3.compatibility[member2.getId()] > 0.85):
                                found = True
                                break
                    if not found:
                        self.notFeasibleReason = f"Not possible to form a committee: No member found with high compatibility for members {member1.id} and {member2.id}"
                        return False
        return True

    def __str__(self):
        total_compatibility, average_compatibility = self.calculate_compatibility_metrics()
        strSolution = 'Total Compatibility (z) = %10.8f\n' % total_compatibility
        strSolution += 'Average Compatibility = %10.8f\n' % average_compatibility
        strSolution += 'Committee Members:\n'
        if not self.committee:
            strSolution += '  No members in the committee.\n'
        else:
            for teacher in self.committee:
                strSolution += '  Teacher ID: %d, Department: %d\n' % (teacher.idN, teacher.department)

        strSolution += '\nDepartment Representatives:\n'
        for department, count in self.department_representatives.items():
            strSolution += '  Department %d: %d members\n' % (department, count)


        return strSolution


    def saveToFile(self, filePath, heuristic_name, local_search, policy, nb_of_iteration, elapsed_time):
        if not self.feasible:
            committees = "impossible"
            total_compatibility = 0.0
            average_compatibility = 0.0
        else:
            total_compatibility, average_compatibility = self.calculate_compatibility_metrics()
            total_compatibility = round(total_compatibility, 2)
            average_compatibility = round(average_compatibility, 2)
            committees = {teacher.idN: teacher.department for teacher in self.committee}

        data_to_write = {
            'D': len(self.departments),
            'n': list(self.departments.values()),
            'N': len(self.teachers),
            'd': [teacher.department for teacher in self.teachers],
            'compatibility_total': total_compatibility,
            'mean_compatibility': average_compatibility,
            'committees': committees,
            'heuristic_name': heuristic_name,
            'localsearch': local_search,
            'policy': policy,
            'nb_of_iteration': nb_of_iteration,
            'elapsed_time': round(elapsed_time, 2),
        }

        file_path = Path(filePath)
        file_exists = file_path.exists()

        with open(file_path, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(data_to_write.keys())

            writer.writerow([
                data_to_write['D'],
                data_to_write['n'],
                data_to_write['N'],
                data_to_write['d'],
                data_to_write['compatibility_total'],
                data_to_write['mean_compatibility'],
                data_to_write['committees'],
                data_to_write['heuristic_name'],
                data_to_write['localsearch'],
                data_to_write['policy'],
                data_to_write['nb_of_iteration'],
                data_to_write['elapsed_time'],
            ])