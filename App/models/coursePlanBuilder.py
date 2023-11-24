from App.database import db

class CoursePlanBuilder(db.Model):
    builderID = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        
        
    