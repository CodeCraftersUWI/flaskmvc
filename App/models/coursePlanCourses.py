
from App.database import db


class CoursePlanCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planId = db.Column(db.ForeignKey('courseplan.planId'))
    code = db.Column(db.ForeignKey('courses.courseCode'))

    
    # courseplan = db.relationship('CoursePlan', back_populates='courses', overlaps="courseplan")


    def __init__(self, plan, courseCode):
        self.planId = plan
        self.code = courseCode
        

    def get_json(self):
        return{
            'Course Plan ID': self.planId,
            'Course': self.code
        }

