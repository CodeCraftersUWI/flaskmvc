from App.database import db

class DegreePlan(db.Model):
    degreePlanID = db.Column(db.Integer, primary_key=True),
    regularPlan = db.Column(db.Integer,  db.ForeignKey('courseplan.planID'), nullable=False),

    def __init__(self, coursePlan ):
        self.regularPlan = coursePlan
        

    def get_json(self):
        return{
            'Degree Plan ID': self.degreePlanID,
            'Plan': self.regularPlan
        }