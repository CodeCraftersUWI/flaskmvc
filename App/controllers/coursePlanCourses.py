from App.models import CoursePlanCourses
from App.database import db

def createPlanCourse(planid, code):
    exists = CoursePlanCourses.query.filter_by(planId=planid, code=code).first()
    if exists:
        print("Course plan course exists already")
        return None
    try:
        course = CoursePlanCourses(planid, code)
        db.session.add(course)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"An error occured when trying to add a course to the course plan: {e}")


def getCourseFromCoursePlan(planid, coursecode):
    return CoursePlanCourses.query.filter_by(planId = planid, code = coursecode).first()

def get_all_courses_by_planid(id):
    return CoursePlanCourses.query.filter_by(planId=id).all()

def deleteCourseFromCoursePlan(planid, coursecode):
    course = getCourseFromCoursePlan(planid, coursecode)
    try:
        db.session.delete(course)
        db.session.commit()
        print("Course succesfully removed from course plan")
    except Exception as e:
        db.session.rollback()
        print("Course is not in Course Plan")
