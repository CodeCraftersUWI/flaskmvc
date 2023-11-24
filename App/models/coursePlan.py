from App.database import db

class CoursePlan(db.Model):
    planID = db.Column(db.Integer, primary_key=True),
    studentID = db.Column(db.Integer,  db.ForeignKey('student.studentID'), nullable=False),
    semesterID = db.Column(db.Integer,  db.ForeignKey('semester.semesterID'), nullable=False),
    programs = db.relationship('Program', backrefs= 'coursePlan', lazy = True),
    courses = db.relationship('Course', backrefs= 'coursePlan', lazy = True)

    def __init__(self, studentid, ):
        self.studentId = studentid
        

    def get_json(self):
        return{
            'planId': self.planId,
            'studentId': self.studentId,
        }