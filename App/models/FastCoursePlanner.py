from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy
from typing import List
from App.controllers import (
    get_student_by_id,
    get_program_by_id,
    getPassedCourseCodes,
    getProgramCoursesByType,
    create_CoursePlan,
    get_course_by_courseCode,
    get_program_course_by_code
    #add as needed
)

# Concrete Strategy: Fast
class FastCoursePlanner(CoursePlannerStrategy):
    def planCourses(self, data: List[str]) -> CoursePlan:
        student_id = data[0]
        current_year = data[1]
        split_year = current_year.split("/")
        next_year = split_year[1] + "/" + str(int(split_year[1])+1)
        print(next_year)
        student = get_student_by_id(student_id)
        program = get_program_by_id(student.program_id)
        program_core_courses = getProgramCoursesByType(program.name, 1)
        program_elec_courses = getProgramCoursesByType(program.name, 2)
        program_foun_courses = getProgramCoursesByType(program.name, 3)
        passed_courses = getPassedCourseCodes(student_id)
        program_course_plan = []

        sem = 1
        # sem_course_plan = create_CoursePlan(student_id, current_year, sem)

        