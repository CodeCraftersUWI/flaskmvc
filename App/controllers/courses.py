from App.models import Course
from App.controllers.prerequistes import (create_prereq, get_prerequisites)
from App.database import db
import json, csv

def createPrerequisites(courseCode, preReqCodes):    
    course =  Course.query.filter_by(courseCode = courseCode).first()

    if course:
        for prereq in preReqCodes:
            prerequisite = Course.query.filter_by(courseCode = prereq).first()

            if prerequisite:
                success = create_prereq(course, prereq)
            else: 
                return("Course " + prereq + " not found. Create a new course before adding it as a prerequisite.")
        
        if (success == False):
            return ("One or more prerequisites already exist for this course.")
    else:
        return ("Unable to add prerequisite. Course not found.")
    
    return ("Successfully added Prerequisite!")

    

def create_course(code, name, credits, rating, semester, level, offered, prereqs):

    already = get_course_by_courseCode(code)
    if already is None:
        course = Course(code, name, credits, rating, semester, level, offered)
        db.session.add(course)
        db.session.commit()

        if (prereqs[0] != ""):
            createPrerequisites(code, prereqs)

        return course
    else:
        return None



def createCoursesfromFile(file_path):
    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                courseCode = row["courseCode"]
                courseName = row["courseName"]
                credits = int(row["numCredits"])
                rating = int(row["rating"])
                semester = int(row["semster"])
                level = int(row["level"])
                offered = bool(row["offered"])
                prerequisites_codes = row["preReqs"].split(',')
                # create_course(courseCode, courseName, rating, credits, prerequisites_codes)
                create_course(courseCode, courseName, credits, rating, semester, level, offered, prerequisites_codes)

    except FileNotFoundError:
        print("File not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
    print("Courses added successfully.")
    
def get_course_by_courseCode(code):
    return Course.query.filter_by(courseCode=code).first()

def courses_Sorted_byRating():
    courses =  Course.query.order_by(Course.rating.asc()).all()
    codes = []

    for c in courses:
        codes.append(c.courseCode)
    
    return codes

def courses_Sorted_byRating_Objects():
    return Course.query.order_by(Course.rating.asc()).all()
    

def isCourseOffered(courseCode):
    course = Course.query.filter_by(courseCode=courseCode).first()
    return course.offered

def get_all_OfferedCodes():
    offered = list_all_courses()
    offeredcodes=[]

    for c in offered:
        offeredcodes.append(c.code)
    
    return offeredcodes

def get_prerequisites(code):
    # course = get_course_by_courseCode(code)
    # prereqs = get_all_prerequisites(course.courseName)
    return get_prerequisites(code)

def get_credits(code):
    course = get_course_by_courseCode(code)
    return course.credits if course else 0

def get_ratings(code):
    course = get_course_by_courseCode(code)
    return course.rating if course else 0

def list_all_courses():
    return (Course.query.all())


