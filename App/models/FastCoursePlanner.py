from App.controllers.coursePlan import getPlanCourses
from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy, Course
from typing import List
from App.controllers import (
    get_student_by_id,
    get_program_by_id,
    getPassedCourseCodes,
    getProgramCoursesByType,
    create_CoursePlan,
    getAllAvailableCourseOptions,
    is_prerequisite,
    get_course_by_courseCode,
    addCourseToPlan,
    numCoursesInPlan,
    get_program_course_by_code,
    getCourseOfferingsByYearAndSemester,
    get_all_programCourses,
    possessPrereqs,
    getCourseOptions
    #add as needed
)
from App.models.courses import Course

# Concrete Strategy: Fast
class FastCoursePlanner(CoursePlannerStrategy):    
    def planCourses(self, data: List[str]):
        student_id = data[0]
        current_year = data[1]
        semester = data[2]
        split_year = current_year.split("/")
        next_year = split_year[1] + "/" + str(int(split_year[1])+1)
        student = get_student_by_id(student_id)
        program = get_program_by_id(student.program_id)
        program_core_courses = getProgramCoursesByType(program.name, 1)
        program_elec_courses = getProgramCoursesByType(program.name, 2)
        program_foun_courses = getProgramCoursesByType(program.name, 3)
        passed_courses = getPassedCourseCodes(student_id)
        added = []
        course_plan = create_CoursePlan(student_id, current_year, semester)
        options = getAllAvailableCourseOptions(student_id, current_year, semester)
        if options:
            altered = False
            for course_code in options:
                course = get_course_by_courseCode(course_code)
                if numCoursesInPlan(course_plan.planId) < 5:
                    if course.level == 1 :
                        addCourseToPlan(student_id, course_code, current_year, semester)
                        added.append(course_code)
                        altered = True
                        # print(f'{course_code} {current_year} 1')
            if altered == True:
                for a in added:
                    options.remove(a)
            altered = False
            for course_code in options:
                if numCoursesInPlan(course_plan.planId) < 5:
                    if is_prerequisite(course_code):
                        addCourseToPlan(student_id, course_code, current_year, semester)
                        added.append(course_code)
                        altered = True
                        # print(f'{course_code} {current_year} 1')
            if altered == True:
                for a in added:
                    options.remove(a)
            for course_code in options:
                if numCoursesInPlan(course_plan.planId) < 5:
                    if is_prerequisite(course_code):
                        addCourseToPlan(student_id, course_code, current_year, semester)
                        added.append(course_code)
                        # print(f'{course_code} {current_year} 1')
            
            codes=[]
            plan_courses = getPlanCourses(student_id, current_year, semester)
            if plan_courses:
                print("Courses in plan:")
                for pc in plan_courses:
                    codes.append(pc.code)
                    print(pc.code)
            return codes
        # programCourses = get_all_programCourses(program.name)
        # programCourseCodes = []
        # for programCourse in programCourses:
        #     programCourseCodes.append(programCourse.code)

        # s1_offerings = getCourseOfferingsByYearAndSemester(current_year, semester)
        # s1_offeringCourseCodes = []
        # if s1_offerings:
        #     for offering in s1_offerings:
        #         s1_offeringCourseCodes.append(offering.course_code)
        
        # s2_offerings = getCourseOfferingsByYearAndSemester(current_year, semester)
        # s2_offeringCourseCodes = []
        # if s2_offerings:
        #     for offering in s2_offerings:
        #         s2_offeringCourseCodes.append(offering.course_code)


        # program_course_plan = []
        # level_1_courses = []
        # level_2_courses = []
        # level_3_courses = []
        

        # options = getCourseOptions(student_id, passed_courses, s1_offeringCourseCodes, programCourseCodes)
        # if options:
        #     for o in options:
        #         print(o)
        # y1s1_course_plan = create_CoursePlan(student_id, current_year, 1)
        # for course_code in options:
        #     course = get_course_by_courseCode(course_code)
        #     if course.level == 1 :
        #         if numCoursesInPlan(y1s1_course_plan.planId) <= 5:
        #             addCourseToPlan(student_id, course.courseCode, current_year, 1)
        #             passed_courses.append(course_code)
        #             print(f'{course.courseCode} {current_year} 1')
        #         else:
        #             program_course_plan.append(y1s1_course_plan)
        #             print("y1s1 full")
        # options = getCourseOptions(student_id, passed_courses, s1_offeringCourseCodes, programCourseCodes)
        
        # if len(program_course_plan) == 1:
        #     split_year = current_year.split("/")
        #     current_year = split_year[1] + "/" + str(int(split_year[1])+1) 
        #     y2s1_course_plan = create_CoursePlan(student_id, current_year, 1)
        #     for course_code in options:
        #         course = get_course_by_courseCode(course_code)
        #         if course.level == 1 :
        #             if numCoursesInPlan(y2s1_course_plan.planId) <= 5:
        #                 addCourseToPlan(student_id, course.courseCode, current_year, 1)
        #                 passed_courses.append(course_code)
        #                 print(f'{course.courseCode} {current_year} 1')
        #             else:
        #                 program_course_plan.append(y2s1_course_plan)
        #                 print("y2s1 full")
        # else:
        #     for course_code in options:
        #         course = get_course_by_courseCode(course_code)
        #         if course.level == 1 :
        #             if numCoursesInPlan(y1s1_course_plan.planId) <= 5:
        #                 addCourseToPlan(student_id, course.courseCode, current_year, 1)
        #                 passed_courses.append(course_code)
        #                 print(f'{course.courseCode} {current_year} 1')
        #             else:
        #                 program_course_plan.append(y1s1_course_plan)
        #                 print("y1s1 full")

    

        # for course_code in options:
        #     course = get_course_by_courseCode(course_code)
        #     if course.level == 1:
        #         print(course_code)
        #         level_1_courses.append(course)
        #     elif course.level == 2:
        #         level_2_courses.append(course)
        #     elif course.level == 3:
        #         level_3_courses.append(course)

        # if len(level_1_courses) != 0:
        #     
        #     for course in level_1_courses:
                
        #             level_1_courses.remove(course)
        #             print(f'{course.courseCode} {current_year} {semester}')
        #         else:
        #             program_course_plan.append(y1s1_course_plan)

        # if len(level_1_courses) != 0:
        #     y1s1_course_plan = create_CoursePlan(student_id, current_year, semester)
        #     # for course in level_1_courses:
                

        # if len(level_1_courses) != 0:
        #     
        #     for course in level_1_courses:
        #         if numCoursesInPlan(y2s1_course_plan.planId) <= 5:
        #             addCourseToPlan(student_id, course.courseCode, current_year, semester)
        #             level_1_courses.remove(course)
        #             print(f'{course.courseCode} {current_year} {semester}')
        
        #     if len(level_1_courses) <= 5:
        #         for course in level_1_courses:
        #                 course = get_course_by_courseCode(course.courseCode)                
        #                 if course.level == 1:
        #                     addCourseToPlan(student_id, course.courseCode, current_year, semester)
        #                     level_1_courses.remove(course)
        #                     print(f'{course.courseCode} {current_year} {semester}')
        
        # # if()


        #         for course_code in options:
                    
        #             addCourseToPlan(student_id, course_code, current_year, semester)
        #             options.remove(course_code)
                # elif is_prerequisite(course_code):
                #     addCourseToPlan(student_id, course_code, current_year, semester)
                #     options.remove(course_code)
                #     print(f'{course_code} {current_year} {semester}')

                # if num_courses > 5 and num_courses <= 10:
                #     split_year = current_year.split("/")
                #     current_year = split_year[1] + "/" + str(int(split_year[1])+1)
                #     addCourseToPlan(student_id, course_code, current_year, semester)
                #     options.remove(course_code)
                #     num_courses += 1
                #     print(f'{course_code} {current_year} {semester}')
                # elif num_courses > 5 and num_courses <= 10:
                    
                #     num_courses += 1
                #     print(f'{course_code} {current_year} {semester}')
        # for course_code

                
            

        


        