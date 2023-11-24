from App.database import db

class FastestGraduation(db.Model):
    fastestGraduationID = db.Column(db.Integer, primary_key=True),
    fastestPlan = db.Column(db.Integer,  db.ForeignKey('courseplan.planID'), nullable=False),

    def __init__(self, coursePlan ):
        self.fastestPlan = coursePlan
        

    def get_json(self):
        return{
            'Degree Plan ID': self.fastestGraduationID,
            'Plan': self.fastestPlan
        }