from App.database import db


class Prerequisites(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    # courseName = db.Column(db.String(25))

    course_code = db.Column(db.String(8), db.ForeignKey('courses.courseCode'))
    prereq_code = db.Column(db.String(8), db.ForeignKey('courses.courseCode'))

    # associated_course = db.relationship('Course', back_populates='prerequisites', overlaps="courses")
      
    # course = db.relationship("Course", foreign_keys=[course_code])
    # prerequisite = db.relationship("Course", foreign_keys=[prereq_code])


    def __init__(self, course_code, prereq_code):
        self.course_code = course_code  
        self.prereq_code = prereq_code

   


    def get_json(self):
        return{
            'prereq_id': self.id,
            'prerequisite_courseCode': self.prereq_code,
            # 'prerequisite_name': self.prerequisite.courseName
            # 'prerequisite_course':self.courseName
        } 