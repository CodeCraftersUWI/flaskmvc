from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy, student
from typing import List
from App.controllers import (
    getAllAvailableCourseOptions,
    get_student_by_id,
    get_all_programCourses
    #add as needed
)

# Concrete Strategy: Easy
class EasyCoursePlanner(CoursePlannerStrategy):
    def planCourses(self, data: int) -> CoursePlan:
        # implement logic
        student = get_student_by_id(data)
        program = student.associated_program
        program_courses = get_all_programCourses(program.id)
        print (program.get_json())

        for x in program_courses:
            print(x.get_json())





        pass