from App.database import db
from .programmeCourse import ProgrammeCourse

class CoursePlanCourse(db.Model):
    __tablename__ = 'course_plan_course'
    id = db.Column(db.Integer, primary_key = True)
    programme_course_id = db.Column(db.Integer,db.ForeignKey("programme_course.id"))
    difficulty = db.Column(db.Integer, nullable=False)#1 to 5, low to high


    def __init__(self, programme_source,difficulty):
        self.programme_course_id = programme_source
        self.difficulty = difficulty
    def get_course_info(self):
        return ProgrammeCourse.query.get(programme_course_id).to_json()
    
    def to_json(self):
        return{
            'Course Plan Course ID': self.id,
            'difficulty': self.difficulty,
            'course_info' : self.get_course_info()
        }

