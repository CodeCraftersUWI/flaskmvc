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

    def autogenerateCoursePlan(self, category):
    

    def updateStudentHistory(self, year, semesterType):

    
    def viewCoursePlan(self, planID):
    

    def addCourseHistory(self, historyID, courseCode, gradeKetter, percent, type):


    def addCourseToPlan(self, planID, courseCode):

    
    def removeCourseFromPlan(self, planID, courseCode):

    def get_json(self):
        return{'Student ID': self.studentID,
            'Name': self.firstName self.lastName,
            'Email' : self.email,
            'Degree Program(s)': self.programs
        }

