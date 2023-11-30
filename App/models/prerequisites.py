from App.database import db


class Prerequisites(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(8), db.ForeignKey('courses.courseCode'))
    prereq_code = db.Column(db.String(8), db.ForeignKey('courses.courseCode'))



    def __init__(self, course_code, prereq_code):
        self.course_code = course_code  
        self.prereq_code = prereq_code

    def get_json(self):
        return{
            'prereq_id': self.id,
            'prerequisite_courseCode': self.prereq_code,
        }