from App.database import db

class CoursePlanDirector(db.Model):
    directorID = db.Column(db.Integer, primary_key=True),
    builderID = db.Column(db.Integer, db.ForeignKey(courseplanbuilder.builderID), nullable = False)

    def __init__(self, builderID):
        self.builderID = builderID
        
    