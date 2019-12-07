
def show_table(classes):
    table = [["COURSE ID","COURSE CODE","SECTION","INSTRUCTOR","TIMESLOT","VENUE","CAPACITY","ENROLLED ","UNITS", "PRREREQUISITES"]]
    for c in classes:
       table.append(c.get_attributes())
    for row in table:
        print("{: <15} {: <15} {: <15} {: <15} {: <15} {: <15} {: <10} {: <10} {: <10} {: <30}".format(*row))  

class course:

    def __init__(self,courseID,courseCode,section,prof,timeslot,venue,max_cap,units,prereqs):
        self.courseID = courseID
        self.courseCode = courseCode
        self.section = section
        self.prof = prof
        self.timeslot = timeslot
        self.venue = venue
        self.max_cap = max_cap
        self.units = units
        self.students = []
        self.prereqs = prereqs

    def addStudent(self,student):
        self.students.append(student)

    def removeStudent(self,student):
         self.students.remove(student)

    def get_attributes(self): 
    
        return [self.courseID,
        self.courseCode,
        self.section,
        self.prof,
        self.timeslot,
        self.venue,
        self.max_cap, 
        len(self.students),
        self.units,
        ",".join(self.prereqs)]

class user():
    
    def __init__(self,user,pw):
        self.username = user
        self.password = pw


class admin(user):

    def __init__(self, user, pw):
        super().__init__(user, pw)

    def createClass(self, courseID, courseCode, section, prof, timeslot,venue, max_cap,units,prereqs,classes):
        classes.append(course(courseID, courseCode, section, prof, timeslot,venue, max_cap,units,prereqs))

    def deleteClass(self, course, classes):
        for s in course.students:
            s.drop(course)

        classes.remove(course)

    def seeClasses(self,classes):   
        show_table(classes)     

    def changeGrades(self,grade,courseCode,student):
        for g in student.grade_report:
            if courseCode == g[0]:
                g[1]=grade


class student(user):

    def __init__(self, user, pw):
        super().__init__(user, pw)
        self.classes_taken = []
        self.grade_report = []

    def enroll(self,course):
        self.classes_taken.append(course)
        course.addStudent(self)
        self.grade_report.append([course.courseCode,-1])

    def drop(self,course):
        self.classes_taken.remove(course)
        course.removeStudent(self)
        for g in self.grade_report:
            if g[0] == course.courseCode and g[1] == -1:
                self.grade_report.remove(g)

    def showEnrolled(self):
        show_table(self.classes_taken)

    def showGrades(self):
        header = ["Course Code","Grade"]
        print("{: <15} {: <15}".format(*header))
        for g in self.grade_report:
            if g[1]!=-1:
                print("{: <15} {: <15}".format(*g))
            else:
                na = [g[0],"N/A"] 
                print("{: <15} {: <15}".format(*na))


    def searchClasses(self,courseCode,classes):
        same_classes = []
        for c in classes:
            if c.courseCode == courseCode:
                same_classes.append(c)

        show_table(same_classes)


    
        
class enlistment:

    def __init__(self):
        self.classes = []
        self.admins = []
        self.students = []
        self.curr_user = ""


    def regStudent(self, user,pw):
        for s in self.students:
            if s.username==user:
                print("Student already exists")
                return

        s_reg = student(user, pw)
        self.students.append(s_reg)

    def regAdmin(self, user,pw):
        for a in self.admins:
            if a.username==user:
                print("Admin already exists")
                return

        a_reg = admin(user,pw)
        self.admins.append(a_reg)

    def loginAdmin(self,user,pw):
        for a in self.admins:
            if user == a.username and pw == a.password:
                self.curr_user = a
                return True
        print("Invalid Username or Password\n")
        
        return False

    def loginStudent(self,user,pw):
        for s in self.students:
            if user == s.username and pw == s.password:
                self.curr_user = s
                return True
        print("Invalid Username or Password\n")
        return False

    def addClass(self,courseID, courseCode, section, prof, timeslot, venue, max_cap,units,prereqs):
        for c in self.classes:
            if courseID == c.courseID:
                print("Class with same course ID already present\n")
                return 
        self.curr_user.createClass(courseID, courseCode, section, prof, timeslot,venue, max_cap,units,prereqs,self.classes)

    def removeClass(self,courseID):
        for c in self.classes:
            if courseID == c.courseID:
                self.curr_user.deleteClass(c,self.classes)
                return
        print("No such class exists")

    def addGrades(self,grade,courseID,student_user):
        for s in self.students:
            if s.username == student_user:
                for c in s.classes_taken:
                    if c.courseID == courseID:
                        self.curr_user.changeGrades(grade,c.courseCode,s)
                        return
                print("Student is not enrolled in class")
                return                
        print("No such student exists")   

    def enrollStudent(self,courseID):
        for c in self.classes:
            if c.courseID == courseID:
                if c in self.curr_user.classes_taken:
                    print("Already enrolled in class")
                    return
                
                completed_classes = []
                for g in self.curr_user.grade_report:
                    if g[1] > 0 and g[0] not in completed_classes:
                        completed_classes.append(g[0])
                if not(set(c.prereqs).issubset(set(completed_classes))):
                    print("Student does not meet the req'd prerequisites")
                    return

                if len(c.students) >= c.max_cap:
                    print("Class is Full")
                    return

                for ct in self.curr_user.classes_taken:
                    if ct.timeslot == c.timeslot: 
                        print("Class with same timeslot already taken") 
                        return

                self.curr_user.enroll(c)
                return
        print("Class does not exist")   
                

            
    def removeStudent(self,courseID):
        for c in self.classes:
            if courseID == c.courseID:
                for ct in self.curr_user.classes_taken:
                    if c == ct:
                        self.curr_user.drop(c)
                        return
                print("Not enrolled in class")
        print("No such class exists")

    def showStudentGrades(self):
        self.curr_user.showGrades()

    
    def logout(self):
        self.curr_user = ""

    def run(self):
        end = False
        login=0
        while not end:
            
            while not login:
                try:
                    c = int(input("What would you like to do? \n1 - Register as Student\n2 - Register as Admin\n3 - Log in as Student\n4 - Log in as Admin\n5 - End\n"))
                    if c == 5:
                        end = True
                        login = 3
                        continue

                    elif c in range(1,5):
                        user = input("Enter Username: ")
                        pw = input("Enter Password: ")
                        if c == 1:
                            self.regStudent(user,pw) 
                        
                        elif c == 2:
                            self.regAdmin(user,pw)
                                
                        elif c == 3:
                            if self.loginStudent(user,pw):
                                login=1
                            
                        elif c == 4:
                            if self.loginAdmin(user,pw):
                                login=2        
                    else:
                        print("INVALID CHOICE")
                except Exception as e:
                    print(e)

            while login == 1:
                try:
                    cStud = int(input("What would you like to do? \n1 - Enroll in Class\n2 - Drop Class\n3 - Search Classes\n4 - See Enrolled Classes\n5 - See Grades\n6 - Logout\n"))
                    if cStud == 1:
                        courseID = input("Enter Course ID\n")
                        self.enrollStudent(courseID)
                    
                    
                    elif cStud == 2:
                        courseID = input("Enter Course ID\n")
                        self.removeStudent(courseID)
                    
                            
                    elif cStud == 3:
                        courseCode = input("Enter Course Code\n")
                        self.curr_user.searchClasses(courseCode,self.classes)

                    elif cStud == 4:
                        self.curr_user.showEnrolled()

                    elif cStud == 5:
                        self.showStudentGrades()
                        
                        
                    elif cStud == 6:
                        self.logout()
                        login=0
                        
                    else:
                        print("INVALID CHOICE")
                except Exception as e:
                   print(e)

            while login == 2:
                try:
                    cAdmin = int(input("What would you like to do? \n1 - Add Class\n2 - Remove Class\n3 - See Classes\n4 - Change Student Grades\n5 - Log out\n"))
                    if cAdmin == 1:
                        courseID = input("Enter Course ID\n")
                        courseCode = input("Enter Course Code\n")
                        section = input("Enter Course Section\n")
                        prof = input("Enter Course Instructor\n")
                        timeslot = input("Enter Course Timeslot\n")
                        venue = input("Enter Course Venue\n")
                        max_cap = int(input("Enter Course Capacity\n"))
                        units = int(input("Enter Course Units\n"))
                        prereqs = []
                        addpr = int(input("Are there Prerequisites? 1-Y 0-N\n"))
                        while addpr==1:
                            prereqs.append(input("Enter Prerequisite Course Code\n"))
                            addpr = int(input("Add more? 1-Y 0-N\n"))

                        self.addClass(courseID, courseCode, section, prof, timeslot, venue,max_cap,units,prereqs)
                    
                    elif cAdmin == 2:
                        courseID = input("Enter Course ID\n")
                        self.removeClass(courseID)
                            
                    elif cAdmin == 3:
                        self.curr_user.seeClasses(self.classes)

                    elif cAdmin == 4:
                        student_user = input("Enter Student\n")
                        courseID = input("Enter Course ID\n")
                        grade = float(input("Enter Grade\n"))
                        self.addGrades(grade,courseID,student_user)

                    elif cAdmin == 5:
                        self.logout()
                        login=0
                            
                    else:
                        print("INVALID")
                except Exception as e:
                    print(e)

enlist = enlistment()
enlist.run()