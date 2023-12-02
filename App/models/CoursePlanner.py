from typing import List
from App.database import db
from App.models import CoursePlannerStrategy, CoursePlan

# Context
class CoursePlanner:
    def __init__(self, strategy: CoursePlannerStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: CoursePlannerStrategy):
        self._strategy = strategy

    def plan_courses(self, data: List[str], target: CoursePlan) -> CoursePlan:
        return self._strategy.search(data, target)