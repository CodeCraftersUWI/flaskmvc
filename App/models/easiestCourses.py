from App.database import db

class EasiestCourses(db.Model):
    easiestCourseID = db.Column(db.Integer, primary_key=True),
    easiestPlan = db.Column(db.Integer,  db.ForeignKey('courseplan.planID'), nullable=False),

    def __init__(self, coursePlan ):
        self.easiestPlan = coursePlan
        

    def get_json(self):
        return{
            'Degree Plan ID': self.easiestCourseID,
            'Plan': self.easiestPlan
        }