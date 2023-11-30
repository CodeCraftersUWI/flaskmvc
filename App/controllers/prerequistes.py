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



def get_all_prerequisites(courseName):
    return Prerequisites.query.filter(Prerequisites.courseName == courseName).all()

def getPrereqCodes(courseName):
    prereqs = get_all_prerequisites(courseName)
    codes = []

    for p in prereqs:
        codes.append(p.prereq_courseCode)
    
    return codes