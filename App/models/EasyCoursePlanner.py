from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy, student
from typing import List
from App.controllers import (
    getAllAvailableCourseOptions
    #add as needed
)

# Concrete Strategy: Easy
class EasyCoursePlanner(CoursePlannerStrategy):
    def planCourses(self, data: int) -> CoursePlan:
        # implement logic


        print("Yes the easycourse planner is being called") 



        pass