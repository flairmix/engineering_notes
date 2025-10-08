from typing import List, Literal
from Building import Building
from Level import Level

#TODO

class Stairwell:
    def __init__(self,
                 building: Building,
                 type: Literal['N1', 'N2', 'N3'],
                 height_m: float,
                 squre_m2: float,
                 levels: List[Level] = None, 
                 ):
        
        self.building = building
        self.type = type 
        self.levels = levels if levels is not None else [] 