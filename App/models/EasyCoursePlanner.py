from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy
from typing import List
from App.controllers import (
    getAllAvailableCourseOptions
    #add as needed
)

# Concrete Strategy: Easy
class EasyCoursePlanner(CoursePlannerStrategy):
    def planCourses(self, data: List[str]) -> CoursePlan:
        # implement logic
        pass