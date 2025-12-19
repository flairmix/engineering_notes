class Level_parking:
    def __init__(self,
                 name: str,
                 level: float = -4.050,
                 area_m2: float = 17077,
                 height_m: float = 4.0,
                 perimeter_m: float = 540.0,
                 
                 ):
        self.name = name
        self.level = level
        self.area_m2 = area_m2
        self.height_m = height_m
        self.perimeter_m = perimeter_m

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "area_m2": self.area_m2,
            "height_m": self.height_m,
            "perimeter_m": self.perimeter_m,
        }
