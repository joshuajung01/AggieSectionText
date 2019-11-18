class course:
    def __init__(self, dept, num, section):
        self.dept = dept
        self.num = num
        self.section = section

    def printName(self):
        return str(self.dept)+" "+str(self.num)+" "+str(self.section)
