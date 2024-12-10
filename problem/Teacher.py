class Teacher(object):
    def __init__(self, idN, department, compatibility):
        self.idN = idN
        self.department = department
        self.compatibility = compatibility  # A dictionary mapping member ids to compatibility values
        self.selected = False

    def getId(self):
        return self.idN

    def getDepartmentId(self):
        return self.department

    def __str__(self):
        return "_idT: %d (in department: %f)" % (self.idN, self.department)