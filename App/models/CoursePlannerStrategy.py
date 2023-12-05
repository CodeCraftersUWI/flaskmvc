from App.database import db
from App.models import CoursePlan
from typing import List
from abc import ABC, abstractmethod

# Strategy Interface
class CoursePlannerStrategy(ABC):
    @abstractmethod
    def planCourses(self, data: List[str]):
        pass

