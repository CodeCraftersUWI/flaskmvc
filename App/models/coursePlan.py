from App.database import db

class CoursePlan(db.Model):
    planID = db.Column(db.Integer, primary_key=True),
    studentID = db.Column(db.Integer,  db.ForeignKey('student.studentID'), nullable=False),
    semesterID = db.Column(db.Integer,  db.ForeignKey('semester.semesterID')),
    program = db.Column(db.Integer, db.ForeignKey('program.programID')),
    courses = db.relationship('Course', secondary = 'CoursePlanCourses' backrefs= 'coursePlan', lazy = True)

    def __init__(self, studentid):
        self.studentId = studentid
        self.semesterID = semesterID
        

    def get_json(self):
        return{
            'Plan ID': self.planId,
            'Student ID': self.studentId,
            'Semester ID': self.semesterID
        }