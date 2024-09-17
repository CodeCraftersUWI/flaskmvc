# from App.models import Prerequisites
from App.database import db
from App.models import Prerequisites

import json

class Course(db.Model):
    __tablename__ = 'courses'

    courseCode = db.Column(db.String(8), primary_key=True)
    courseName = db.Column(db.String(25))
    credits = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    semester = db.Column(db.Integer)
    level = db.Column(db.Integer)   #the degree year that the course is typically taken
    offered = db.Column(db.Boolean) #whether or not the course is currently offered

    students = db.relationship('StudentCourseHistory', backref='courses', lazy=True)
    programs = db.relationship('ProgramCourses', backref='courses', lazy=True)
    coursePlan = db.relationship('CoursePlanCourses', backref='courses', lazy=True)
    prerequisites = db.relationship('Prerequisites', foreign_keys=[Prerequisites.course_code], lazy = True)


   
    
    def __init__(self, code, name, credits, rating, semester, level, offered):
        self.courseCode = code
        self.courseName = name
        self.credits = credits
        self.rating = rating
        self.semester = semester
        self.level = level
        self.offered = offered
        
    
    def get_json(self):
        return{
            'Course Code:': self.courseCode,
            'Course Name: ': self.courseName,
            'Credits: ': self.credits,
            'Semester: ': self.semester,
            'Level: ': self.level, 
            'Course Rating: ': self.rating,
            'No. of Credits: ': self.credits,

        }