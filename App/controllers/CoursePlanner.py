from App.models import CoursePlan, Student
from App.database import db 
from App.controllers import (
    get_student_by_id, 

)

def createCoursePlan(student_id, Mode): #mode is easy, fastest or prioritise electives
    student = get_student_by_id(student_id)
    



