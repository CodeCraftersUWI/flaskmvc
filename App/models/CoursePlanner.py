from typing import List
from App.database import db
from App.models import CoursePlannerStrategy, CoursePlan, student

# Context
class CoursePlanner:
    def __init__(self, strategy: CoursePlannerStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: CoursePlannerStrategy):
        self._strategy = strategy


    def plan_courses(self, data: List[str]):
        return self._strategy.planCourses(data)