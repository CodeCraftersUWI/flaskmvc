from App.models import ProgramCourses, Program, Course
from App.controllers import (get_program_by_name, get_program_by_id, get_course_by_courseCode)
from App.database import db

def create_programCourse(programName, code, num):
    try:
        program = get_program_by_name(programName)
        if program:
            course = get_course_by_courseCode(code)
            if course:
                proCourse = ProgramCourses.query.filter_by(program_id=program.id, code=code, courseType=num).first()
                if proCourse:
                    print("Course already added to program")
                else:
                    proCourse = ProgramCourses(program.id, code, num)
                    db.session.add(proCourse)
                    db.session.commit()
                    return proCourse
            else:
                return "Invalid course code"
        else:
            return "Invalid program name"
    except Exception as e:
        db.session.rollback()
        print(f'Error occured when trying to add course to program: {e}')

def get_all_programCourses(programName):
    program = get_program_by_name(programName)
    return ProgramCourses.query.filter(ProgramCourses.program_id == program.id).all()

    
def get_all_programCourses(program_id):
    program = get_program_by_id(program_id)
    return ProgramCourses.query.filter(ProgramCourses.program_id == program_id).all()

# new function to get core, elective or foun courses
def getProgramCoursesByType(programName, type):
    program = get_program_by_name(programName)
    programCourses = ProgramCourses.query.filter_by(program_id=program.id, courseType=type).all()
    courseCodes = []
    for programCourse in programCourses:
        courseCodes.append(programCourse.code)
    return courseCodes

# repetitive
# def get_allCore(programName):
#     program = get_program_by_name(programName)
#     core = ProgramCourses.query.filter_by(program_id=program.id, courseType=1).all()
#     return core if core else []

# def get_allElectives(programName):
#     program = get_program_by_name(programName)
#     core = ProgramCourses.query.filter_by(program_id=program.id, courseType=2).all()
#     return core if core else []

# def get_allFoun(programName):
#     program = get_program_by_name(programName)
#     core = ProgramCourses.query.filter_by(program_id=program.id, courseType=3).all()
#     return core if core else []

def convertToList(programCourses):
    courseCodes = []

    for programCourse in programCourses:
        courseCodes.append(programCourse.code)
    
    return courseCodes

# new function to get courses with a specific rating
def getProgramCoursesByRating(programName, rating):
    courses = []
    program = get_program_by_name(programName)
    programCourses = ProgramCourses.query.all.filter_by(program_id=program.id).all()
    for programCourse in programCourses:
        course = get_course_by_courseCode(programCourse.code)
        if course.rating == rating:
            courses.append(course)
    if courses == []:
        print("No courses found in the given program with the given rating")
    return courses if courses else []

# from previous code - not tested
def programCourses_SortedbyRating(programid):
    program = get_program_by_id(programid)
    programCourses = get_all_programCourses(program.name)

    sorted_courses = {1: [], 2: [], 3: [], 4: [], 5: []}

    for p in programCourses:
        course = get_course_by_courseCode(p.code)
        sorted_courses[course.rating].append(course.courseCode)
    
    sorted_courses_list = [course for rating_courses in sorted_courses.values() for course in rating_courses]

    return sorted_courses_list

# from previous code - seems unnecessary
def programCourses_SortedbyHighestCredits(programid):
    program = get_program_by_id(programid)
    programCourses = get_all_programCourses(program.name)

    highTolow = []

    for p in programCourses:
        course = get_course_by_courseCode(p.code)
        if course.credits > 3:
            highTolow.insert(0,course.courseCode)
        else:
            highTolow.append(course.courseCode)

    return highTolow
