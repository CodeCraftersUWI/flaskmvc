from App.models import User  
from App.database import db

class Student(User):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    studentHistory = db.relationship('SemesterHistory', back_populates='student')
    studentHistory = db.Column(db.Integer, db.ForeignKey('group.groupId'), nullable=False)

    program_id = db.Column(db.ForeignKey('program.id'))
    
    associated_program = db.relationship('Program', back_populates='students', overlaps="program")
    courses = db.relationship('StudentCourseHistory', backref='student', lazy=True)

    def __init__(self, username, password, name, program_id):
        super().__init__(username, password)
        self.id = username
        self.name = name
        self.program_id = program_id

    def get_json(self):
        return{'student_id': self.id,
            'name': self.name,
            'program' : self.program_id
            
        }

