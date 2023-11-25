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

    coreCourses = relationship('Course', secondary='program_core_courses', backref='core_programs')
    electiveCourses = relationship('Course', secondary='program_elective_courses', backref='elective_programs')
    founCourses = relationship('Course', secondary='program_foun_courses', backref='foun_programs')

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
