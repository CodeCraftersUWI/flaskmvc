from .user import User 
from App.database import db
from sqlalchemy import Column, Integer, Date, ForignKey

class Staff(User):
    
    staffID = db.Column(db.Integer, primary_key=True)
    departmentCode = db.Column(db.String(10), db.ForeignKey(department.departmentCode), nullable = False)
    firstName = db.Column(db.String(50), nullable = False)
    firstName = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(254),nullable = False )

    department = relationship('Department', backref='staff_members')
    created_programs = relationship('Program', backref='creator', foreign_keys='Program.creatorID')
    created_courses = relationship('Course', backref='creator', foreign_keys='Course.creatorID')
    created_semesters = relationship('Semester', backref='creator', foreign_keys='Semester.creatorID')

    def create_program(self, name, core_credits, elective_credits, foun_credits, department_code):
        program = Program(programName=name, coreCredits=core_credits, electiveCredits=elective_credits, founCredits=foun_credits, departmentCode=department_code, creator=self)
        db.session.add(program)
        db.session.commit()
      
    def create_course(self, course_name, course_code, credits, difficulty):
        course = Course(courseName=course_name, courseCode=course_code, credits=credits, difficulty=difficulty, creator=self)
        db.session.add(course)
        db.session.commit()

    def create_semester(self, year, semester_type):
        semester = Semester(year=year, semesterType=semester_type, creator=self)
        db.session.add(semester)
        db.session.commit()

    def remove_program(self, program_name):
        program = Program.query.filter_by(programName=program_name, creator=self).first()
        if program:
            db.session.delete(program)
            db.session.commit()
            
    def __repr__(self):
        return f"<Staff {self.staffID} - {self.firstName} {self.lastName}>"
       

       

