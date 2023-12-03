from App.database import db

class CoursePlan(db.Model):
    __tablename__ = 'courseplan'


    planId=db.Column(db.Integer, primary_key=True)
    studentId=db.Column(db.Integer,  db.ForeignKey('student.id'), nullable=False)
    course_code = db.Column(db.ForeignKey('courses.courseCode'))



    # student = db.relationship('Student', backref=db.backref('course_plans', uselist=True))
    courseplancourses = db.relationship('CoursePlanCourses', backref = 'courseplan', lazy=True)

    def __init__(self, studentid):
        self.studentId = studentid

        

    def get_json(self):
        return{
            'planId': self.planId,
            'studentId': self.studentId,
            'courses' : [plancourse.get_json() for plancourse in self.courseplancourses]
        }