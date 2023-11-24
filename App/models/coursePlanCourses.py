from App.database import db


class CoursePlanCourses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coursePlanID = db.Column(db.ForeignKey('courseplan.planID'))
    courseCode = db.Column(db.ForeignKey('course.courseCode'))

    def __init__(self, plan, courseCode):
        self.coursePlanID = plan
        self.courseCode = courseCode
        

    def get_json(self):
        return{
            'Course Plan ID': self.coursePlanID,
            'Course': self.courseCode
        }

