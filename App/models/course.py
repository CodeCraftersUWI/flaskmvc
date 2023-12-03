from App.database import db
from .course_self_bridge import course_self_bridge
# from App.models import prerequisites
# import json

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True)
    courseTitle = db.Column(db.String(20), unique=True, nullable=False)
    courseCode = db.Column(db.String(120), nullable=False)
    courseCredits = db.Column(db.Integer, nullable=False)
    courseDept = courseCode = db.Column(db.String(120), nullable=False)
    # typing = db.Column(db.String(120), nullable=False)
    prerequistes = db.relationship('Course', secondary=course_self_bridge, backref = 'successorCourses')
    antiRequisites = db.relationship('Course', secondary=course_self_bridge, backref = 'antiRequisites')
    successorCourses = db.relationship('Course', secondary=course_self_bridge, backref = 'prerequistes')
    def __init__(self,title,code,credits,dept):
        self.courseTitle = title
        self.courseCode = code
        self.set_credits(credits)
        self.courseDept = dept
        self.prerequistes = None
        self.antiRequisites = None
        self.successorCourses = None


    def set_credits(self,credits):
        self.courseCredits = credits

    def add_course_to_list(self,course,list):
        if list == 'p':
            self.prerequistes.append(course)
        if list == 'a':
            self.antiRequisites.append(course)
        if list == 's':
            self.successorCourses.append(course)
        

    def remove_course_from_list(self,course,list):
        if list == 'p':
            self.prerequistes.remove(course)
        if list == 'a':
            self.antiRequisites.remove(course)
        if list == 's':
            self.successorCourses.remove(course)

    def get_course_title(self):
        return self.courseTitle   

    def get_course_code(self): 
        return self.courseCode   

    def get_course_credits(self):
        return self.courseCredits 

    def get_course_dept(self):
        return self.courseDept

    def get_prereq(self):
        return [course.to_json() for course in self.prerequistes]
        # return self.prerequistes

    def get_anti_req(self):
        return [course.to_json() for course in self.antiRequisites]
        # return self.antiRequisites

    def get_succesors(self):
        return [course.to_json() for course in self.successorCourses]
        # return self.successorCourses

    def to_json(self):
        return{
            "course_id" : self.course_id,
            "title": self.get_course_title(),
            "code":self.get_course_code(),
            "credits":self.get_course_credits(),
            "department":self.get_course_dept(),
            "prerequistes" : self.get_prereq(),
            "anti_requistes" : self.get_anti_req(),
            "successorCourses" : self.get_succesors()
        }
    # courseCode = db.Column(db.String(8), primary_key=True)
    # courseName = db.Column(db.String(25))
    # credits = db.Column(db.Integer)
    # rating = db.Column(db.Integer)

    # offered = db.relationship('CoursesOfferedPerSem', backref ='courses', lazy=True)
    # students = db.relationship('StudentCourseHistory', backref='courses', lazy=True)
    # programs = db.relationship('ProgramCourses', backref='courses', lazy=True)
    # prerequisites = db.relationship('Prerequisites', backref='courses', lazy = True)

    # # planIds = db.relationship('CoursePlanCourses', backref='courses', lazy=True)
   
    
    # def __init__(self, code, name, rating, credits):
    #     self.courseCode = code
    #     self.courseName = name
    #     self.rating = rating
    #     self.credits = credits
    
    # def to_json(self):
    #     return{
    #         'Course Code:': self.courseCode,
    #         'Course Name: ': self.courseName,
    #         'Course Rating: ': self.rating,
    #         'No. of Credits: ': self.credits,
    #     }