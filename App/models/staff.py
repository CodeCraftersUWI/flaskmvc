from .user import User 
from App.database import db

class Staff(User):

    dept = db.Column(db.String(120),nullable=False)
    faculty = db.Column(db.String(20),nullable=False)


    def __init__(self, username, password, name):
        super().__init__(username,password,name)
    
    def set_dept(self,dept):
        self.dept = dept
    def set_faculty(self,faculty):
        self.faculty = faculty

    def to_json(self):
        base = super().to_json()
        return{
            base + 
            "department" : self.dept,
            "faculty" : self.faculty
        }

