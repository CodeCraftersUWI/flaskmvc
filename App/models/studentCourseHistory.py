from App.database import db

class StudentCourseHistory(db.Model):
    __tablename__ = 'studentCourses'
    
    id = db.Column(db.Integer, primary_key=True)  
    student_id = db.Column(db.String, db.ForeignKey('student.id'))
    course_code = db.Column(db.String, db.ForeignKey('courses.courseCode'))
    grade = db.Column(db.String) 
    
    associated_course = db.relationship('Course', back_populates='students')
    associated_student = db.relationship('Student', back_populates='courses')

    def __init__(self, student_id, course_code):
        self.student_id = student_id
        self.course_code = course_code
    
    def get_json(self):
        return {
            'StudentCourseHistory ID': self.id,
            'Student ID': self.student_id,
            'Course Code': self.course_code,
            'Grade': self.grade
        }