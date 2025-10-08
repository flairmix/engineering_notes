from typing import Literal


class Building:
    def __init__(self, 
                 name: str, 
                 height_m: float,
                 type = Literal["Жилое", "Общественное"],
                 ):
        self.name = name
        self.height_m = height_m
        self.type = type

    def __str__(self):
        return f"Building {self.name}"