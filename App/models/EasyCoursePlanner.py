from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy, student
from typing import List
from App.controllers import (
    getAllAvailableCourseOptions,
    get_student_by_id,
    get_all_programCourses,
    getCompletedCourses, 
    getProgramCoursesByRating,
    getProgramCoursesByType
    #add as needed
)

# Concrete Strategy: Easy
class EasyCoursePlanner(CoursePlannerStrategy):
    def planCourses(self, data: int) -> CoursePlan:
        # implement logic
        student = get_student_by_id(data)
        program = student.associated_program
        # program_courses = getProgramCoursesByRating(program.name, 5)
        program_courses = get_all_programCourses(program.name)
        core_courses = getProgramCoursesByType(program.name, 1)
        courseHistory =  getCompletedCourses(student.id)
        completed_core_courses = []
        incomplete_core_courses = []

        for pastCourse in courseHistory: 
            for core in core_courses:
                if (core.code == pastCourse.code):
                    completed_core_courses.append(core)
        
        # for core in core_courses: 
 
        for x in completed_core_courses:
            print( x.get_json())
        
        print("Courses that need to be completed:")

        for i in incomplete_core_courses:
            print(i.get_json())
        





        pass