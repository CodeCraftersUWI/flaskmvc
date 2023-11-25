from App.database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Program(db.Model):
    __tablename__ = 'programs'

    programID = Column(Integer, primary_key=True)
    departmentCode = Column(String(10), ForeignKey('departments.departmentCode'), nullable=False)
    programName = Column(String, nullable=False)
    coreCredits = Column(Integer, nullable=False)
    electiveCredits = Column(Integer, nullable=False)
    founCredits = Column(Integer, nullable=False)

    coreCourses = db.relationship('ProgramCourse', sbackref=db.backref('course', lazy='joined'))
    electiveCourses = db.relationship('ProgramCourse', backref=db.backref('course', lazy='joined'))
    founCourses = db.relationship('ProgramCourse', backref=db.backref('course', lazy='joined'))
    students = db.relationship('Student', backref=db.backref('student', lazy='joined'))

    def __init__(self, department_code, program_name, core_credits, elective_credits, foun_credits):
        self.departmentCode = department_code
        self.programName = program_name
        self.coreCredits = core_credits
        self.electiveCredits = elective_credits
        self.founCredits = foun_credits
        
    students = relationship('Student', backref='program')

    def add_course(self, course_code, course_type):
        
        course = Course.query.get(course_code)
        if course:
            if course_type == 'core':
                self.coreCourses.append(course)
            elif course_type == 'elective':
                self.electiveCourses.append(course)
            elif course_type == 'foundation':
                self.founCourses.append(course)
            db.session.commit()

    def __repr__(self):
        return f"<Program {self.programID} - {self.programName}>"
