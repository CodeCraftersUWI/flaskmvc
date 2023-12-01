from App.models import StudentCourseHistory
from App.controllers import (get_student_by_id, get_course_by_courseCode)
from App.database import db

def addCourseToHistory(student_id, course_code, grade=None):

    try:
        student = get_student_by_id(student_id)
        course = get_course_by_courseCode(course_code)

        if not student: 
            raise ValueError("Student does not exist")

        if not course:
            raise ValueError("Course does not exist")

        enrollment = StudentCourseHistory(
            student_id=student_id,
            course_code=course_code,
            grade=grade
        )

        db.session.add(enrollment)  
        db.session.commit()

    except ValueError as e:
        print(e)  

    return enrollment
         

def getCompletedCourses(id):
    return StudentCourseHistory.query.filter_by(studentID=id).all()

def getCompletedCourseCodes(id):
    completed = getCompletedCourses(id)
    codes = []
    
    for c in completed:
        codes.append(c.code)
    
    return codes
