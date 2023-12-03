from App.database import db
from .course import Course
class HistoryCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_course_id = db.Column(db.Integer,db.ForeignKey("course.course_id"))
    passed = db.Column(db.Boolean, nullable=False)

    def __init__(self,base,passed):
        self.base_course_id = base
        self.passed = passed
    def get_course_info(self,base_id):
        return Course.query.get(base_id).to_json()
    def course_passed(self):
        return self.passed
    def to_json(self):
        return{
            'history_course_id' : self.id,
            'course_info' : self.get_course_info(),
            'passed' : self.course_passed()
        }