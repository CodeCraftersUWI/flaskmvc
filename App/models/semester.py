from App.database import db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Semester(db.Model):
    semesterID= db.Column(db.Integer, primary_key = True) 
    courses= db.relationship('SemesterCourse', backref=db.backref('course', lazy='joined'))
    year= db.Column(db.Datetime, nullable = False)
    semestertype= db.Column(db.Integer, nullable = False)

    def add_course(course):
        if course not in self.courses:
            self.sourses.append(course)
            db.session.commit()

    def remove_course(course):
        self.courses.remove(course)
        db.session.commit()
