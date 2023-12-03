from App.database import db
from .plan_course_bridge import plan_course_bridge
class CoursePlan(db.Model):
    __tablename__ ='CoursePlan'
    id = db.Column(db.Integer, primary_key=True)
    # studentId=db.Column(db.Integer,  db.ForeignKey('student.id'), nullable=False)
    student = db.Column(db.Integer, db.ForeignKey("student.id"),nullable=False)
    courses = db.relationship('course_plan_course',secondary=plan_course_bridge,backref='in_course_plans')
    semester = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, student, year,sem):
        self.student = student
        self.year = year
        self.sem = sem
        
    def get_plan_courses(self):
        return [course.to_json() for course in self.courses]

    def to_json(self):
        return{
            'id': self.id,
            'student_id': self.student,
            'semester' : self.semester,
            'year':self.year,
            'plan_courses' : get_plan_courses()
        }