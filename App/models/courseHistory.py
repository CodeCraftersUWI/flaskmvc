from App.database import db

class CourseHistory(db.Model):
    CourseHistoryID = db.Column(db.Integer, primary_key=True),
    courseCode = db.Column(db.String(50), db.ForeignKey('course.courseCode')),
    gradeLetter = db.Column(db.Char, nullable = False),
    percent = db.Column(db.Double, nullable= False),
    courseType = db.Column(db.String(50), nullable = False),
    semesterID = db.Column(db.Integer ),
    semesterHistory = db.relationship('Semester History', backrefs= 'courses')

    def __init__(self, id, courseCode, gradeLetter, percent, courseType, semID):
        self.courseHistoryID = id
        self.courseCode = courseCode
        self.gradeLetter = gradeLetter
        self.percent percent
        self.semesterID = semID
    

    def get_json(self):
        return{
            'CourseHistory ID': self.courseHistoryID, #is this suppose to be id or program_id alone 
            'Course Code': self.courseCode,
            'Course Grade': self. gradeLetter self.percent
        }
