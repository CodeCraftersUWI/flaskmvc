from App.database import db

class SemesterHistory(db.Model):
    historyID = db.Column(db.Integer, primary_key=True),
    studentID = db.Column(db.ForeignKey('student.studentID')),
    year = db.Column(db.Integer, nullable = False),
    semeterType = db.Column(db.Integer, nullable= False),
    courses = db.relationship('CourseHistory', backrefs= 'semesterHistory', lazy = True)

    def __init__(self, id, year, semesterType):
        self.studentID = id
        self.year = year
        self.semesterType = semesterType
    
    def get_json(self):
        return{
            'Student ID': self.studentID, #is this suppose to be id or program_id alone 
            'Semester Date': f'{self.year} - Semester {self.semesterType}',
            'Courses': self.courses
        }