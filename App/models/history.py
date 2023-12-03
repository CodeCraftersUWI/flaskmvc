from App.database import db

class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))
    year = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    # semesterCourses = db.relationship('Course',secondary=HistoryCourseBridge,backref='previousStudents')
    semesterCourses = db.relationship('HistoryCourse', backref=db.backref('history'), lazy = 'joined')

    def __init__(self,student,year,semester):
        self.student_id = student
        self.year = year
        self.semester = semester

    def add_course_to_history(self,course):
        self.semesterCourses.append(course)

    def to_json(self): 
        courselist = [course.to_json() for course in self.semesterCourses]
        return{
            'student' : self.student_id,
            'year' : self.year,
            'semester' :self.semester,
            'courses done': courselist 
        }