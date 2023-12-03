from App.database import db
from App.models import CourseOfferings

def createCourseOffering(courseCode, academic_year, semester):
    courseCode=courseCode.replace(" ","").upper()   #ensure consistent course code format
    offering = CourseOfferings.query.filter_by(course_code=courseCode, academic_year=academic_year, semester=semester).first()
    if offering:
        print("Course offering exists already")
        return None
    try:
        if CourseOfferings.checkAcademicYearFormat(academic_year):
            if semester == 1 or semester == 2 or semester == 3:
                if CourseOfferings.getCourse(courseCode):
                    offeredCourse = CourseOfferings(academic_year, semester, courseCode)
                    if offeredCourse:
                        db.session.add(offeredCourse)
                        db.session.commit()
                        print("Course offering created successfully")
                        return offeredCourse
                    else: 
                        print("The new course offering could not be created")
                else: 
                    print(f"Invalid course code")
            else:
                print(f"The semester is invalid. There are 3 semesters: 1, 2, 3")
        else:
            print(f"Academic year format incorrect. Should be  yyyy/yyyy e.g. 2022/2023")
    except Exception as e:
        db.session.rollback()
        print(f"An error occured when trying to add a course to the course offerings: {e}")

def getAllCourseOfferings():
    return CourseOfferings.query.all()

def getCourseOfferingsByYear(year):
    if CourseOfferings.checkAcademicYearFormat(year):
        offerings = CourseOfferings.query.filter_by(academic_year = year).all()
        if offerings:
            return offerings
        else:
            print("There are no offerings for the selected year")
    else:
        print("Academic year format incorrect. Should be yyyy/yyyy e.g. 2022/2023")

def getCourseOfferingsBySemester(sem):
    if sem == 1 or sem == 2 or sem == 3:
        offerings = CourseOfferings.query.filter_by(semester = sem).all()
        if offerings:
            return offerings
        else:
            print("There are no offerings for the selected semester")
    else:
        print(f"The semester is invalid. There are 3 semesters: 1, 2, 3")

def getCourseOfferingsByYearAndSemester(year, sem):
    if CourseOfferings.checkAcademicYearFormat(year):
        if sem == 1 or sem == 2 or sem == 3:
            offerings = CourseOfferings.query.filter_by(semester = sem, academic_year = year).all()
            if offerings:
                return offerings
            else:
                print("There are no offerings for the selected year and semester")
        else:
            print(f"The semester is invalid. There are 3 semesters: 1, 2, 3")
    else:
        print("Academic year format incorrect. Should be yyyy/yyyy e.g. 2022/2023")

def deleteCourseOffering(courseCode, academic_year, semester):
    courseCode=courseCode.replace(" ","").upper()   #ensure consistent course code format
    try:
        offering = CourseOfferings.query.filter_by(course_code=courseCode, academic_year=academic_year, semester=semester).first()
        if offering:
            db.session.delete(offering)
            db.session.commit()
            print("Course offering deleted successfully")
            return True
        else: 
            print("The course offering you are trying to delete does not exist")
    except Exception as e:
        db.session.rollback()
        print(f"An error occured when trying to delete the course from the course offerings: {e}")
        return False
    
def isCourseOffering(courseCode, academic_year, semester):
    offering = CourseOfferings.query.filter_by(course_code=courseCode, academic_year=academic_year, semester=semester).first()
    if offering:
        return True
    else:
        return False
