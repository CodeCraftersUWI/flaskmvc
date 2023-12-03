from App.database import db
from .course import Course
class ProgrammeCourse(db.Model):
    __tablename__ ='programme_course'
    id = db.Column(db.Integer, primary_key=True)
    base_course_id = db.Column(db.Integer,db.ForeignKey("course.course_id"))
    # program_id = db.Column(db.ForeignKey('program.id'))
    # code = db.Column(db.ForeignKey('course.courseCode'))
    courseType = db.Column(db.String(120), nullable=False)
    semesterAvailable= db.Column(db.String(120), nullable=False)
    # associated_program = db.relationship('Program', back_populates='courses', overlaps="program")
    # associated_course = db.relationship('Course', back_populates='programs', overlaps="courses")

    def __init__(self, base_id, course_type,semester_available):
        self.base_course_id = base_id
        self.set_course_type(course_type)
        self.set_semester_available(semester_available)

    def set_course_type(self,typing):
        self.courseType = typing

    def set_semester_available(self,sem):
        self.semesterAvailable = sem

    def course_available(self,current_sem):
        return current_sem == self.semesterAvailable

    def get_course_info(self,base_id):
        return Course.query.get(base_id).to_json()
        
    def to_json(self):
        return{
            'programme_course_id' : self.id,
            'course_info' : self.get_course_info(),
            'course_type': self.courseType,
            'semester_available' : self.semesterAvailable
        }