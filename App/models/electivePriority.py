from App.database import db

class ElectivePriority(db.Model):
    electivePlanID = db.Column(db.Integer, primary_key=True),
    electivePlan = db.Column(db.Integer,  db.ForeignKey('courseplan.planID'), nullable=False),

    def __init__(self, coursePlan ):
        self.electivePlan = coursePlan
        

    def get_json(self):
        return{
            'Degree Plan ID': self.electivePlanID,
            'Plan': self.electivePlan
        }