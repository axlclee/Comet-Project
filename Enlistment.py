

#CLASS FOR CLASSES
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

    #METHODS TO ADD AND REMOVE STUDENTS 
    def addStudent(self,student):
        self.students.append(student)

    def removeStudent(self,student):
         self.students.remove(student)

    #METHOD TO RETURN ALL NECESSARY VALUES TO BE DISPLAYED
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

#PARENT CLASS FOR USERS
class user():
    
    def __init__(self,user,pw):
        self.username = user
        self.password = pw

    #METHOD TO DISPLAY CLASSES
    def show_table(self,classes):
        table = [["COURSE ID","COURSE CODE","SECTION","INSTRUCTOR","TIMESLOT","VENUE","CAPACITY","ENROLLED ","UNITS", "PRREREQUISITES"]]
        for c in classes:
            table.append(c.get_attributes())
        for row in table:
            print("{: <15} {: <15} {: <15} {: <15} {: <15} {: <15} {: <10} {: <10} {: <10} {: <30}".format(*row))  

#ADMINISTRATOR CLASS
class admin(user):

    def __init__(self, user, pw):
        super().__init__(user, pw)

    #METHOD TO CREATE CLASS
    def createClass(self, courseID, courseCode, section, prof, timeslot,venue, max_cap,units,prereqs,classes):
        classes.append(course(courseID, courseCode, section, prof, timeslot,venue, max_cap,units,prereqs))

    #METHOD TO DELETE CLASS
    def deleteClass(self, course, classes):
        #drop all students currently enrolled
        for s in course.students:
            s.drop(course)
        #remove class from class list
        classes.remove(course)

    #METHOD TO SEE ALL CLASSES
    def seeClasses(self,classes):   
        self.show_table(classes)     

    #METHOD TO CHANGE GRADE OF A STUDENT IN A CLASS
    def changeGrades(self,grade,courseCode,student):
        for g in student.grade_report:
            if courseCode == g[0]:
                g[1]=grade

#STUDENT CLASS
class student(user):

    def __init__(self, user, pw):
        super().__init__(user, pw)
        self.classes_taken = []
        self.grade_report = []

    #METHOD TO ENROLL STUDENT
    def enroll(self,course):

        #add course to classes currently taken
        self.classes_taken.append(course)
        #add self to list of students in class
        course.addStudent(self)
        #initialize grade report with grade -1 to symbolize class is not yet completed
        self.grade_report.append([course.courseCode,-1])

    #METHOD TO DROP CLASS
    def drop(self,course):
        #remove course from list of classes taken
        self.classes_taken.remove(course)
        #remove self from list of students in class
        course.removeStudent(self)
        #remove class from grade report list if not yet completed
        for g in self.grade_report:
            if g[0] == course.courseCode and g[1] == -1:
                self.grade_report.remove(g)

    #METHOD TO SHOW ALL CLASSES CURRENTLY ENROLLED IN
    def showEnrolled(self):
        self.show_table(self.classes_taken)

    #METHOD TO SHOW ALL GRADES
    def showGrades(self):
        header = ["Course Code","Grade"]
        print("{: <15} {: <15}".format(*header))
        for g in self.grade_report:
            if g[1]!=-1:
                print("{: <15} {: <15}".format(*g)) 
            else:
                #REPLACE -1 WITH N/A IN REPORT 
                na = [g[0],"N/A"] 
                print("{: <15} {: <15}".format(*na))

    #METHOD TO SEARCH FOR CLASSES BY COURSE CODE
    def searchClasses(self,courseCode,classes):
        #create list of all classes sharing the name of the course code
        same_classes = []
        for c in classes:
            if c.courseCode == courseCode:
                same_classes.append(c)

        self.show_table(same_classes)


    
 #CLASS FOR MANAGING THE ENLISTMENT SYSTEM       
class enlistmentManager:

    def __init__(self):
        self.classes = []
        self.admins = []
        self.students = []
        self.curr_user = ""

#MANAGER METHODS

    #METHOD TO REGISTER STUDENT INTO SYSTEM
    def regStudent(self, user,pw):
        for s in self.students:
            #usernames must be unique per student
            if s.username==user:
                print("Student already exists")
                return
        #if username is unique, create new student object and add it to record of students
        s_reg = student(user, pw)
        self.students.append(s_reg)

    #METHOD TO REGISTER ADMIN INTO SYSTEM
    def regAdmin(self, user,pw):
        for a in self.admins:
            #usernames must be unique per admin
            if a.username==user:
                print("Admin already exists")
                return
        #if username is unique, create new admin object and add it to record of admin
        a_reg = admin(user,pw)
        self.admins.append(a_reg)

    #METHOD TO LOG IN AS ADMIN    
    def loginAdmin(self,user,pw):
        #if entered username and password is valid, set curr_user to admin object with matching attributes and return true, else return false
        for a in self.admins:
            if user == a.username and pw == a.password:
                self.curr_user = a
                return True
        print("Invalid Username or Password\n")
        return False

    #METHOD TO LOG IN AS STUDENT   
    def loginStudent(self,user,pw):
         #if entered username and password is valid, set curr_user to student object with matching attributes and return true, else return false
        for s in self.students:
            if user == s.username and pw == s.password:
                self.curr_user = s
                return True
        print("Invalid Username or Password\n")
        return False

    #METHOD TO LOG OUT
    def logout(self):
        self.curr_user = ""

#ADMIN METHODS

    #METHOD TO ADD A CLASS INTO THE DATABASE
    def addClass(self,courseID, courseCode, section, prof, timeslot, venue, max_cap,units,prereqs):
        #check if course ID is unique before adding
        for c in self.classes:
            if courseID == c.courseID:
                print("Class with same course ID already present\n")
                return 
        self.curr_user.createClass(courseID, courseCode, section, prof, timeslot,venue, max_cap,units,prereqs,self.classes)

    #METHOD TO REMOVE CLASS FROM DATABASE
    def removeClass(self,courseID):
        for c in self.classes:
            if courseID == c.courseID:
                self.curr_user.deleteClass(c,self.classes)
                return
        print("No such class exists")

    #METHOD TO ADD/CHANGE GRADES FOR A STUENNT IN A CLASS
    def addGrades(self,grade,courseID,student_user):
        #look for student in database
        for s in self.students:
            if s.username == student_user:
                #look through all their classes taken
                for c in s.classes_taken:
                    if c.courseID == courseID:
                        self.curr_user.changeGrades(grade,c.courseCode,s)
                        return
                print("Student is not enrolled in class")
                return                
        print("No such student exists")   

    #METHOD TO DISPLAY ALL CLASS OFFERINGS 
    def showAllClasses(self):
        self.curr_user.seeClasses(self.classes)

#STUDENT METHODS

    #METHOD TO ENROLL A STUDENT INTO A CLASS
    def enrollStudent(self,courseID):
        for c in self.classes:
            #check if course ID matches ID of class already taken
            if c.courseID == courseID:
                if c in self.curr_user.classes_taken:
                    print("Already enrolled in class")
                    return
                
                #check if completed classes of the student meet the prerequisite requirements of the class
                completed_classes = []
                for g in self.curr_user.grade_report:
                    #if grade for a course is passing and course code was not already added to list of passed classes
                    if g[1] > 0 and g[0] not in completed_classes:
                        completed_classes.append(g[0])
                if not(set(c.prereqs).issubset(set(completed_classes))):
                    print("Student does not meet the req'd prerequisites")
                    return

                #check max capacity of a class
                if len(c.students) >= c.max_cap:
                    print("Class is Full")
                    return

                #check for time slot conflicts
                for ct in self.curr_user.classes_taken:
                    if ct.timeslot == c.timeslot: 
                        print("Class with same timeslot already taken") 
                        return

                self.curr_user.enroll(c)
                return
        print("Class does not exist")   
                

    #METHOD TO REMOVE STUDENT FROM CLASS        
    def removeStudent(self,courseID):
        #find class in class database
        for c in self.classes:
            if courseID == c.courseID:
                #find class in student's list of classes taken
                for ct in self.curr_user.classes_taken:
                    if c == ct:
                        self.curr_user.drop(c)
                        return
                print("Not enrolled in class")
        print("No such class exists")

    #METHOD TO SHOW GRADE REPORT
    def showStudentGrades(self):
        self.curr_user.showGrades()

    #METHOD TO SEARCH FOR CLASSES
    def studentSearch(self,courseCode):
        self.curr_user.searchClasses(courseCode,self.classes)

    #METHOD TO SHOW ALL CLASSES CURRENTLY ENROLLED IN
    def studentEnrolled(self):
        self.curr_user.showEnrolled()


#CLASS FOR ENLISTMENT DISPLAY
class enlistment:

    def __init__(self):
        #initialize manager
        self.emgr = enlistmentManager()
    
    #METHOD FOR GETTING INPUT
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
                            self.emgr.regStudent(user,pw) 
                        
                        elif c == 2:
                            self.emgr.regAdmin(user,pw)
                                
                        elif c == 3:
                            if self.emgr.loginStudent(user,pw):
                                login=1
                            
                        elif c == 4:
                            if self.emgr.loginAdmin(user,pw):
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
                        self.emgr.enrollStudent(courseID)
                    
                    
                    elif cStud == 2:
                        courseID = input("Enter Course ID\n")
                        self.emgr.removeStudent(courseID)
                    
                            
                    elif cStud == 3:
                        courseCode = input("Enter Course Code\n")
                        self.emgr.studentSearch(courseCode)

                    elif cStud == 4:
                        self.emgr.studentEnrolled()

                    elif cStud == 5:
                        self.emgr.showStudentGrades()
                        
                        
                    elif cStud == 6:
                        self.emgr.logout()
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

                        self.emgr.addClass(courseID, courseCode, section, prof, timeslot, venue,max_cap,units,prereqs)
                    
                    elif cAdmin == 2:
                        courseID = input("Enter Course ID\n")
                        self.emgr.removeClass(courseID)
                            
                    elif cAdmin == 3:
                        self.emgr.showAllClasses()

                    elif cAdmin == 4:
                        student_user = input("Enter Student\n")
                        courseID = input("Enter Course ID\n")
                        grade = float(input("Enter Grade\n"))
                        self.emgr.addGrades(grade,courseID,student_user)

                    elif cAdmin == 5:
                        self.emgr.logout()
                        login=0
                            
                    else:
                        print("INVALID")
                except Exception as e:
                    print(e)




enlist = enlistment()
enlist.run()