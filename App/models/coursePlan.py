from App.database import db

class CoursePlan(db.Model):
    __tablename__ = 'courseplan'


    planId=db.Column(db.Integer, primary_key=True)
    academic_year = db.Column(db.String, nullable=False)
    semester = db.Column(db.String(1), nullable=False)
    studentId=db.Column(db.String(10),  db.ForeignKey('student.id'), nullable=False)

    student = db.relationship('Student', backref=db.backref('course_plans', uselist=True))

    # courses = db.relationship('CoursePlanCourses', backref = 'coursePlan', lazy=True)
    
    def __init__(self, studentid, year, sem):
        self.studentId = studentid
        self.academic_year = year
        self.semester = sem
        

    def get_json(self):
        return{
            'planId': self.planId,
            'year': self.academic_year,
            'semester': self.semester,
            'studentId': self.studentId,
        }
    
    def checkAcademicYearFormat(academic_year):
        s = academic_year.split("/")
        if len(s) != 2:
            return False
        elif int(s[0]) != int(s[1])-1:
            return False
        elif int(s[0]) < 2000:
            return False
        return True