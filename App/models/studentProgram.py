from App.database import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class StudentProgram(db.Model):
    __tablename__ = 'student_programs'

    studentProgramID = Column(Integer, primary_key=True)
    studentID = Column(Integer, ForeignKey('students.studentID'), nullable=False)
    programID = Column(Integer, ForeignKey('programs.programID'), nullable=False)

    program = relationship('Program', backref='student_programs')
    student = relationship('Student', backref='student_programs')

    def __repr__(self):
        return f"<StudentProgram {self.studentProgramID}>"
