from App.database import db
from sqlalchemy.orm import relationship

class Prerequisite(db.Model):
    prereqID = db.Column(db.Integer,primary_key= True)
    courseCode= db.Column(db.String(8),db.ForeignKey('course.courseCode', nullable=False))
    prerequisiteCourses= db.relationship('Prerequisite', backref= db.backref('course', laxy='joined'))
    
    def addPrerequisite(self, prereq_course):
        self.prerequisiteCourses.append(prereq_course)
        db.session.commit()
    

    def edit_course(self, courseName, courseCode, credits, difficulty):
        self.courseName = course_name
        self.courseCode = course_code
        self.credits = credits
        self.difficulty = difficulty
        db.session.commit()
