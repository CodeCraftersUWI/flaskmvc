from App.models import StudentCourseHistory
from App.controllers import (get_student_by_id, get_course_by_courseCode)
from App.database import db


def addCoursetoHistory(studentid, code, grade):
    student  = get_student_by_id(studentid)
    if student:
        course = get_course_by_courseCode(code)
        if course:
            completed = StudentCourseHistory(studentid, code, grade)
            db.session.add(completed)
            db.session.commit()
        else:
            print("Course doesn't exist")
    else:
        print("Student doesn't exist")
'''
def addCoursetoHistory(student_id, course_code, grade):

    try: 
        student = get_student_by_id(student_id)
        course = get_course_by_courseCode(course_code)

        if not student:
            raise ValueError("Invalid student ID")

        if not course:
            raise ValueError("Invalid course code")
        
        enrollment = StudentCourseHistory(
            student_id = student_id,
            course_code = course_code,
            grade = grade
        )

        db.session.add(enrollment)
        db.session.commit()

    except ValueError as e:
        print(e)

    return enrollment         
'''
def getCompletedCourses(id):
    return StudentCourseHistory.query.filter_by(studentID=id).all()

def getCompletedCourseCodes(id):
    completed = getCompletedCourses(id)
    codes = []
    
    for c in completed:
        codes.append(c.code)
    
    return codes
