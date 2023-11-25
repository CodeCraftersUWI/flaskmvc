from App.database import db
from App.models import prerequisites
import json

class Course(db.Model):
    
    courseCode = db.Column(db.String(8), primary_key=True)
    prereqID = db.Column(db.Integer, db.ForeignKey('prerequisite.prereqID', nullable= False))
    courseName = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False, )
    difficulty = db.Column(db.Integer(20), nullable=False)
    
    
   
    

    
    def get_json(self):
        return{
            'Course Code:': self.courseCode,
            'Course Name: ': self.courseName,
            'Course difficulty: ': self.difficulty,
            'No. of Credits: ': self.credits,
        }
