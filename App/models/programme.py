from App.database import db
from .programme_course_bridge import programme_course_bridge
class Programme(db.Model):
    __tablename__ = 'programme'
    programmId = db.Column(db.Integer, primary_key=True)
    degreeName  = db.Column(db.String(50))
    courses = db.relationship('Course',secondary=programme_course_bridge,backref='in_programmes')

    def __init__(self, name):
       self.set_name(name)
       

    def set_name(self,name):
        self.degreeName = name
    def add_course(self,course):
        self.courses.append(course)

    def get_degree_name(self):
        return self.degreeName
    def get_courses(self):
        return [course.to_json() for course in self.courses]

    def to_json(self):
        return{
            'programme_id': self.id,
            'programme_name': self.get_degree_name(),
            'programme_courses' : self.get_courses()
        }
       