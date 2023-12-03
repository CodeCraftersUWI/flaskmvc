from App.database import db
from App.models import CoursePlan, CoursePlannerStrategy
from typing import List

# Concrete Strategy: Fast
class ElectiveCoursePlanner(CoursePlannerStrategy):
    def planCourses(self, data: List[str]) -> CoursePlan:
        # implement logic
        pass