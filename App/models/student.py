# from App.models import User  
from App.database import db
from .user import User

class Student(User):
    __tablename__ = 'Student'
    year_of_study = db.Column(db.Integer, nullable=False)
    programme = db.Column(db.Integer, db.ForeignKey("programmeID"))
    # academicHistory = db.relationship('History', backref=db.backref('Student'), lazy ='joined')
    academicHistory = db.relationship('history', backref=db.backref('student'), lazy = 'joined')
    academicPlan = db.relationship('CoursePlan', backref=db.backref('student'), lazy = 'joined',uselist=False)
    # academicPlan = db.Column(db.Integer, db.ForeignKey("CoursePlanID"))
    # id = db.Column(db.String(10), db.ForeignKey('user.id'), primary_key=True)
    # name = db.Column(db.String(50))
    # program_id = db.Column(db.ForeignKey('program.id'))
    
    # associated_program = db.relationship('Program', back_populates='students', overlaps="program")
    # courses = db.relationship('StudentCourseHistory', backref='student', lazy=True)

    def __init__(self, username, password, name, utype, year):
        self.username = username
        super.set_password(password)
        super.set_name(name)
        self.userType = utype
        self.year_of_study = year


    def get_history(self):
        return self.academicHistory

    def get_programme(self):
        return self.programme

    def get_student_curr_year(self):
        return self.year_of_study

    def enroll_in_programme(self, programme):
        self.programme = programme

    def create_course_plan(self,coursePlan):
        self.academicPlan = coursePlan

    def view_course_plan(self):
        return self.academicPlan

    def add_new_history(self,history):
        self.academicHistory.append(history)

    # def __repr__(self):
    #     return f'<User: {self.id}, {self.name}, {self.username}>'

    def to_json(self):
        base = super().to_json()
        prog = self.get_programme().get_degree_name()
        return{
            base+
            "current year of study" : self.get_student_curr_year(),
            "programme": prog,
            "academic history": self.get_history(),
            "academicPlan": self.view_course_plan()

        }
        


