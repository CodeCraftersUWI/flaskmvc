from App.models import CoursePlan, CoursePlanCourses
from App.database import db 
from App.controllers import (
    get_program_by_id, 
    get_course_by_courseCode, 
    get_credits, 
    getPrereqCodes,
    getCompletedCourses,
    createPlanCourse,
    deleteCourseFromCoursePlan,
    getProgramCoursesByType,
    getPassedCourseCodes,
    convertToList,
    get_all_OfferedCodes,
    isCourseOffered,
    programCourses_SortedbyRating,
    programCourses_SortedbyHighestCredits,
    get_all_courses_by_planid,
    isCourseOffering,
    getCompletedCourseCodes,
    get_student_by_id,
    getCourseOfferingsByYearAndSemester,
    get_all_programCourses
)



def create_CoursePlan(id, year, sem):
    try:
        plan = CoursePlan.query.filter_by(studentId=id, academic_year=year, semester=sem).first()
        if plan:
            print("Course plan exists already")
            return None
        else: 
            if CoursePlan.checkAcademicYearFormat(year):
                if sem == 1 or sem == 2 or sem == 3:
                    plan = CoursePlan(id, year, sem)
                    if plan:
                        db.session.add(plan)
                        db.session.commit()
                        print("Course offering created successfully")
                        return plan
                    else: 
                        print("The course plan could not be created")
                else:
                    print(f"The semester is invalid. There are 3 semesters: 1, 2, 3")
            else:
                print(f"Academic year format incorrect. Should be  yyyy/yyyy e.g. 2022/2023")
    except Exception as e:
        db.session.rollback()
        print(f"An error occured when trying to create the course plan: {e}")

def getCoursePlan(studentid, year, sem):
    return CoursePlan.query.filter_by(studentId=studentid, academic_year=year, semester=sem).first()

def possessPrereqs(studentId, courseCode):
    preqs = getPrereqCodes(courseCode)
    completed = getPassedCourseCodes(studentId)
    for course in preqs:
        if course not in completed:
            return False
    
    return True

    
def getPlanCourses(student_id):
    plan = getCoursePlan(student_id)
    return get_all_courses_by_planid(plan.planId)



def addCourseToPlan(Student, courseCode):
    course = get_course_by_courseCode(courseCode)
    if course:
        print("Course Found!")
        offered = isCourseOffered(courseCode)
        if offered:
            offering = isCourseOffering(courseCode, year, sem)
            if offering:
                haveAllpreqs = possessPrereqs(studentId, course)
                if haveAllpreqs:
                    plan = getCoursePlan(studentId, year, sem)
                    if plan:
                        createPlanCourse(plan.planId, courseCode)
                        print("Course successfully added to course plan")
                        return plan
                    else:
                        plan = create_CoursePlan(studentId, year, sem)
                        createPlanCourse(plan.planId, courseCode)
                        print("Plan successfully created and Course was successfully added to course plan")
                        return plan
                else:
                    print("Missing prerequisites")
            else:
                print("Course not being offered for requested semester")
        else:
            print("Course is not offered")
    else:
        print("Course does not exist")

def removeCourseFromPlan(studentid, year, sem, courseCode):
    plan=getCoursePlan(studentid, year, sem)
    if plan:
        deleteCourseFromCoursePlan(plan.planId, courseCode)

def getRemainingCoursesByType(student_id, type):
    student=get_student_by_id(student_id)
    program=get_program_by_id(student.program_id)
    remaining = []

    if program:
        required=getProgramCoursesByType(program.name, type)
        completed = getPassedCourseCodes(student_id)

    if completed == []:
        return required

    remaining = required.copy()
    for course in completed:
        if course in required:
            remaining.remove(course)

    return remaining

def getRemainingCreditsByCourseType(student_id, type):
    remaining = getRemainingCoursesByType(student_id, type)
    student=get_student_by_id(student_id)
    program=get_program_by_id(student.program_id)
    requiredCreds=0
    if type == 1:
        requiredCreds=program.core_credits
    elif type == 2:
        requiredCreds=program.elective_credits
    elif type == 3:
        requiredCreds=program.foun_credits
    
    for code in remaining:
        course = get_course_by_courseCode(code)
        if course:
            requiredCreds = requiredCreds - course.credits
    
    return requiredCreds

'''
    @getAllAvailableCourseOptions
    filters each course being offered in the specified semester by if:
       - the student passed it already
       - the student's program has it
       - the student has all the prerequisites to take it
    and compiles a list of courses the student can take
'''
def getAllAvailableCourseOptions(student_id, year, sem):
    offerings = getCourseOfferingsByYearAndSemester(year, sem)
    offeringCourseCodes = []
    for offering in offerings:
        offeringCourseCodes.append(offering.course_code)

    student = get_student_by_id(student_id)
    program = get_program_by_id(student.program_id)
    programCourses = get_all_programCourses(program.name)
    programCourseCodes = []
    for programCourse in programCourses:
        programCourseCodes.append(programCourse.code)
    
    passed = getPassedCourseCodes(student_id)

    available=[]

    for code in offeringCourseCodes:
        if code not in passed:
            if code in programCourseCodes:
                if possessPrereqs(student.id, code):
                    available.append(code)

    return available        #returns an array of course codes

# previous code - seems unnecessary
# def getTopfive(list):
#     return list[:5]

# def prioritizeElectives(Student):
#     #get available electives
#     electives=findAvailable(getRemainingElec(Student))      
#     credits=remElecCredits(Student)
#     courses=[]
    
#     #select courses to satisfy the programme's credit requirements
#     for c in electives:     
#         if credits>0:
#             courses.append(c)
#             credits = credits - get_credits(c)
    
#     #merge available, required core and foundation courses
#     courses = courses + findAvailable(getRemainingCore(Student)) + findAvailable(getRemainingFoun(Student))

#     courses = checkPrereq(Student,courses)
#     return getTopfive(courses)


# def removeCoursesFromList(list1,list2):
#     newlist = list2.copy()
#     for a in list1:
#         if a in newlist:
#             newlist.remove(a)
#     return newlist
    

# def easyCourses(Student):
#     program = get_program_by_id(Student.program_id)
#     completed = getCompletedCourseCodes(Student.id)
#     codesSortedbyRating = programCourses_SortedbyRating(Student.program_id)

#     coursesToDo = removeCoursesFromList(completed, codesSortedbyRating)

#     elecCredits = remElecCredits(Student)
    
#     if elecCredits == 0:
#         allElectives = convertToList(get_allElectives(program.name))
#         coursesToDo = removeCoursesFromList(allElectives, coursesToDo)
    
#     coursesToDo = findAvailable(coursesToDo)

#     ableToDo = checkPrereq(Student, coursesToDo)
#     # for a in ableToDo:
#     #     print(a)
    
#     return getTopfive(ableToDo)


# def fastestGraduation(Student):
#     program = get_program_by_id(Student.program_id)
#     sortedCourses = programCourses_SortedbyHighestCredits(Student.program_id)
#     completed = getCompletedCourseCodes(Student.id)

#     coursesToDo = removeCoursesFromList(completed, sortedCourses)

#     elecCredits = remElecCredits(Student)
    
#     if elecCredits == 0:
#         allElectives = convertToList(get_allElectives(program.name))
#         coursesToDo = removeCoursesFromList(allElectives, coursesToDo)
    
#     coursesToDo = findAvailable(coursesToDo)
#     ableToDo = checkPrereq(Student, coursesToDo)

#     return getTopfive(ableToDo)

# def commandCall(Student, command):
#     courses = []

#     if command == "electives":
#         courses = prioritizeElectives(Student)
    
#     elif command == "easy":
#         courses = easyCourses(Student)
    
#     elif command == "fastest":
#         courses = fastestGraduation(Student)
    
#     else:
#         print("Invalid command")
    
#     return courses


# def generator(Student, command):
#     courses = []

#     plan = getCoursePlan(Student.id)

#     if plan is None:
#         plan = plan = create_CoursePlan(Student.id)

    
#     courses = commandCall(Student, command)

#     existingPlanCourses = get_all_courses_by_planid(plan.planId)

#     planCourses = []
#     for q in existingPlanCourses:
#         planCourses.append(q.code)

#     for c in courses: 
#         if c not in planCourses:
#             createPlanCourse(plan.planId, c)

#     return courses