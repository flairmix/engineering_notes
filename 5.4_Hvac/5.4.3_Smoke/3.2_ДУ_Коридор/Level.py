from typing import Optional
from Building import Building

class Level:
    def __init__(self,
                 building: Building,
                 number: int,
                 elevation_rel: float,
                 elevation_abs: Optional[float]= None,
                 ):
        self.building = building
        self.number = number
        self.elevation_rel = elevation_rel
        self.elevation_abs = elevation_abs

    def __str__(self):
        return f"Level in {self.building}| number {self.number}|на отм.{self.elevation_rel}"