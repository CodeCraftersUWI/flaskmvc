from App.models import Prerequisites
from App.database import db

# def create_prereq(prereqCode, courseName):
#     prereq = Prerequisites(prereqCode, courseName)
#     db.session.add(prereq)
#     db.session.commit()

def create_prereq(course, prereqCode):
    exists = Prerequisites.query.filter_by(course_code= course.courseCode, prereq_code= prereqCode).first()

    if exists:
        return False
    

    new_prereq = Prerequisites(course_code=course.courseCode, prereq_code= prereqCode)
    course.prerequisites.append(new_prereq)

    try:
        db.session.add(new_prereq)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("There was an error...")
        print(e)



def get_all_prerequisites(courseCode):
    return Prerequisites.query.filter_by(course_code = courseCode).all()

def get_prerequisites(courseCode):
    return Prerequisites.query.filter_by(course_code = courseCode).all()

def getPrereqCodes(courseCode):
    prereqs = get_prerequisites(courseCode)
    codes = []

    for p in prereqs:
        codes.append(p.prereq_code)
    
    return codes