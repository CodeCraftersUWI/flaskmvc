from App.database import db

class StudentCourseHistory(db.Model):
    __tablename__ = 'studentCourses'
    id = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.ForeignKey('student.id'))
    code = db.Column(db.ForeignKey('course.courseCode'))
    grade = db.Column(db.String)

    associated_course = db.relationship('Course', back_populates='students', overlaps="courses")
    associated_student = db.relationship('Student', back_populates='courses', overlaps="student")

    def __init__(self, student_id, course_code, grade=None):
        self.studentID = student_id
        self.code = course_code
        self.grade = grade
    
    def get_json(self):
        return{
            'Program ID': self.id, #is this suppose to be id or program_id alone 
            'Course Code': self.code,
            'Grade': self.grade
        }