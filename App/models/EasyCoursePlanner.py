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
    create_CoursePlan
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
        

        remaining_core_courses = (program.core_credits - core_credits)/3
        remaining_elec_courses = (program.elective_credits - elec_credits)/3
        remaining_foun_courses = (program.foun_credits- foun_credits)/3

        # print(int(remaining_core_courses))
        # print(int(remaining_elec_courses))
        # print(int(remaining_foun_courses))


        #assuming the easiest courses get a higher rating, we take courses with ratings of 4 and 5 for the easy course plan
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
                if (easy.courseType == 3):
                    easy_foun_courses.append(course)

            if (len(easy_core_courses)>= remaining_core_courses) and (len(easy_elec_courses)>=remaining_elec_courses) and (len(easy_foun_courses)>= remaining_foun_courses):
                break

                # create_CoursePlan(student.id,  )
            # for i in range(remaining_core_courses, 0, -1):



        # print(f'Easy Core Count: {len(easy_core_courses)}')
        # print(f'Easy Elec Count: {len(easy_elec_courses)}')
        # print(f'Easy Foun Count: {len(easy_foun_courses)}')
        
        # for i in easy_elec_courses:
        #     print(f'{i.courseCode} {i.rating}')



        pass