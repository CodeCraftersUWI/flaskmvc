from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy, student
from typing import List
from App.controllers import (
    getAllAvailableCourseOptions,
    get_student_by_id,
    get_all_programCourses,
    getCompletedCourses, 
    getProgramCoursesByRating,
    getProgramCoursesByType,
    get_course_by_courseCode,
    get_program_course_by_code,
    create_CoursePlan,
    getCourseOfferingsByYearAndSemester,
    addCourseToPlan,
    getPlanCourses,
    numCoursesInPlan
    #add as needed
)
 
# Concrete Strategy: Easy
class EasyCoursePlanner(CoursePlannerStrategy):
    def planCourses(self, data: List[str]):
        # implement logic
        student_id = data[0]
        student = get_student_by_id(student_id)
        program = student.associated_program
        # program_courses = getProgramCoursesByRating(program.name, 5)
        program_courses = get_all_programCourses(program.name)
        core_courses = getProgramCoursesByType(program.name, 1)
        elec_courses = getProgramCoursesByType(program.name, 2)
        foun_courses = getProgramCoursesByType(program.name, 3)
        courseHistory =  getCompletedCourses(student.id)
        completed_core_courses = []
        incomplete_core_courses = []
        complete_electives = []
        complete_foun_courses = []

        core_credits = 0
        elec_credits = 0
        foun_credits = 0 

        for pastCourse in courseHistory: 
            for core in core_courses:
                if (core.code == pastCourse.code):
                    completed_core_courses.append(core)
                    core_credits += get_course_by_courseCode(core.code).credits
            for elec in elec_courses:
                if (elec.code == pastCourse.code):
                    complete_electives.append(elec)
                    elec_credits += get_course_by_courseCode(elec.code).credits
            for foun in foun_courses:
                if (foun.code == pastCourse.code):
                    complete_foun_courses.append(foun)
                    foun_credits += get_course_by_courseCode(foun.code).credits

        for core in core_courses:
            if (core not in completed_core_courses):
                incomplete_core_courses.append(core)

    
        print(f'Program Core Credits: {program.core_credits}')
        print(f'Program Elec Credits: {program.elective_credits}')
        print(f'Program Foun Credits: {program.foun_credits}')

        print(f'Student Core Credits: {core_credits}')
        print(f'Student Elec Credits: {elec_credits}')
        print(f'Student Foun Credits: {foun_credits}')
        

        remaining_core_courses = int((program.core_credits - core_credits)/3)
        remaining_elec_courses = int((program.elective_credits - elec_credits)/3)
        remaining_foun_courses = int((program.foun_credits- foun_credits)/3)

        # print(int(remaining_core_courses))
        # print(int(remaining_elec_courses))
        # print(int(remaining_foun_courses))


        #assuming the easiest courses get a higher rating, we take courses with ratings of 5 for the easy course plan
        # if courses with a rating of 5, the next 'easiest' rating will be selected, and so on
        easy_core_courses = []
        easy_elec_courses = []
        easy_foun_courses = []

        for i in range(5, 0, -1):
            easy_program_courses = getProgramCoursesByRating(program.name, i)

            for course in easy_program_courses:
                easy= get_program_course_by_code(course.courseCode)

                if (easy.courseType == 1):
                    easy_core_courses.append(course)
                if (easy.courseType == 2):
                    easy_elec_courses.append(course)
                    # print(course.courseCode)
                if (easy.courseType == 3):
                    easy_foun_courses.append(course)

            if (len(easy_core_courses)>= remaining_core_courses) and (len(easy_elec_courses)>=remaining_elec_courses) and (len(easy_foun_courses)>= remaining_foun_courses):
                break


        counter = 0

        # while(True):

        coursePlanList = []
        sem = 1
        year = "2023/2024"

        

        coursePlanList.append(create_CoursePlan(student.id, year, sem))
        offering = getCourseOfferingsByYearAndSemester(year,sem)
        offered_courses = []

        if offering: 
            for crs in offering:
                offered_courses.append(get_course_by_courseCode(crs.course_code))

        plan = coursePlanList[0]

        for i in range(remaining_core_courses, 0, -1):
            if(numCoursesInPlan(plan.planId) >=5) or (core_credits >= program.core_credits):
                break
            popped = easy_core_courses.pop(0)
            if(popped in offered_courses):
                print("Adding core course")
                core_credits += popped.credits
                addCourseToPlan(student_id, popped.courseCode, year, sem)
                
        

        for i in range(remaining_elec_courses, 0, -1):
            if(numCoursesInPlan(plan.planId) >=5):
                break
            popped = easy_elec_courses.pop(0)

            if(popped in offered_courses):
                elec_credits += popped.credits
                addCourseToPlan(student_id, popped.courseCode, year, sem)
                


        for i in range(remaining_foun_courses, 0, -1):
            if(numCoursesInPlan(plan.planId) >=5):
                break
            popped = easy_foun_courses.pop(0)

            if(popped in offered_courses):
                foun_credits = popped.credits
                addCourseToPlan(student_id, popped.courseCode, year, sem)
                

        print("\n\n")
        print(f'Student Core Credits: {core_credits}')
        print(f'Student Elec Credits: {elec_credits}')
        print(f'Student Foun Credits: {foun_credits}')
        

        plancourses = getPlanCourses(student_id, "2023/2024", sem)

        for i in plancourses: 
            print(f'{get_course_by_courseCode(i.code).courseCode} {get_course_by_courseCode(i.code).credits}')

        pass