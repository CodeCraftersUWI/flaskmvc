from App.models import User  
from App.database import db

class Student(User):
    studentID = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable = False),
    lastName = db.Column(db.String(50), nullable = False),
    email = db.Column(db.String(50), nullable = False, unique = True),
    studentHistory = db.relationship('SemesterHistory', backref='student', lazy = true),
    coursePlans = db.relationship('CoursePlan', backref='student', lazy = true)

    def __init__(self, id, firstName, lastName, email):
        self.studentID = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email

    def autogenerateCoursePlan(self, category, degreeType, programID, semesterID):
        director = new coursePlanDirector()
        builder = None
        
        if category == "Easiest Courses":
            builder = new EasiestCourses(self.studentID)
        else if category == "Fastest Graduation"
            builder = new FastestGraduation(self.studentID)
        else if category == "Elective Priority"
            builder = new ElectivePriority(self.studentID)

        if degreeType == "Minor":
            director.constructMinor(builder, semesterID, programID, self.studentID)
        else if degreeType == "Major":
            director.constructMajor(builder, semesterID, programID, self.studentID)
        else if degreeType == "Special"
            director.constructSpecial(builder, semesterID, programID, self.studentID)

        plan = builder.getPlan()
        if plan:
            return plan
        return None       
        
    

    def updateStudentHistory(self, year, semesterType):
        semHistory = SemesterHistory(self.studentID, year, semesterType)
        self.studentHistory.append(semHistory)
        db.session.add(semHistory)
        db.session.commit()

    
    def viewCoursePlan(self, planID):
        plan = CoursePlan.query.get(planID).first()
        if plan in self.coursePlans:
            return plan
        return None
    

    def addCourseHistory(self, historyID, courseCode, gradeLetter, percent, courseType):
        semHistory = SemesterHistory.query.get(historyID).first()
        if semHistory: 
            if semHistory in self.studentHistory:
                courseHist = CourseHistory(courseCode, gradeLetter, percent, courseType, historyID)
                semHistory.courses.append(courseHist)
                db.session.add(courseHist)
                db.session.commit()
            return None
        return None


    def addCourseToPlan(self, planID, courseCode):
        plan = CoursePlan.query.get(planID).first()
        course = Course.query.get(courseCode).first()
        if plan and course:
            plan.courses.append(course)-
            db.session.commit()
        return None

    def removeCourseFromPlan(self, planID, courseCode):
        plan = CoursePlan.query.get(planID).first()
        course = Course.query.get(courseCode).first()
        if plan and course:
            plan.courses.remove(course)-
            db.session.commit()
        return None

    def get_json(self):
        return{'Student ID': self.studentID,
            'Name': self.firstName self.lastName,
            'Email' : self.email,
            'Degree Program(s)': self.programs
        }

