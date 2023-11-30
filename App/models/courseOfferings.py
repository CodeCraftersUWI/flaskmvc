from App.database import db
from .courses import Course

class CourseOfferings(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    academic_year = db.Column(db.String, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    course_code = db.Column(db.String, nullable=False)

    def get_json(self):
        return{
            'id': self.id,
            'year': self.academic_year,
            'semester': self.semester,
            'course': self.course_code
        }
    
    def getCourse(course_code):
        return Course.query.filter_by(courseCode=course_code).first()            
    
    def checkAcademicYearFormat(academic_year):
        s = academic_year.split("/")
        if s.size() > 2:
            return False
        elif int(s[0]) != int(s[1])-1:
            return False
        elif int(s[0]) < 2000:
            return False
        return True
