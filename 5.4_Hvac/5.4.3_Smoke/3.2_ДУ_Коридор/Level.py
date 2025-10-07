from typing import Optional, Literal



class Building:
    def __init__(self, 
                 name: str, 
                 height_m: float,
                 type = Literal["Жилое", "Общественное"],
                 ):
        self.name = name
        self.height_m = height_m
        self.type = type


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