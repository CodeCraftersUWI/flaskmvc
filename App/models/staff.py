from .user import User 
from App.database import db
from sqlalchemy import Column, Integer, Date, ForignKey

class Staff(User):
    
    staffID = db.Column(db.Integer, primary_key=True)
    departmentCode = db.Column(db.String(10), db.ForeignKey(department.departmentCode), nullable = False)
    firstName = db.Column(db.String(50), nullable = False)
    firstName = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(254),nullable = False )
    


