from typing import List, Literal

#TODO

class Stairwell:
    def __init__(self,
                 type: Literal['N1', 'N2', 'N3'],
                 height_m: float,
                 squre_m2: float,
                 ):
        
        self.type = type 