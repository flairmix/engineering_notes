
class Room:
    def __init__(self,
                 room_number: str,
                 room_name: str,
                 room_area_m2: float,
                 room_high_m: float,
                 room_fire_load_density: float,
                 room_calorific_value_fire_load: float,
                 room_temp_inside_C: int = 24):
        
        self.room_number = room_number
        self.room_name = room_name
        self.room_area_m2 = room_area_m2
        self.room_high_m = room_high_m
        self.room_volume_m3 = room_area_m2 * room_high_m
        self.room_fire_load_density = room_fire_load_density
        self.room_calorific_value_fire_load = room_calorific_value_fire_load
        self.room_temp_inside_C = room_temp_inside_C
        self.temp_inside_K = room_temp_inside_C + 273
        
    def __str__(self):
        return f"class Room: room_number - {self.room_number}, room_name - {self.room_name}"


    def to_dict(self) -> dict:
        """Возвращает все параметры помещения в виде словаря"""
        return {
            "number": self.room_number,
            "name": self.room_name,
            "area_m2": self.room_area_m2,
            "height_m": self.room_high_m,
            "volume_m3": self.room_volume_m3,
            "fire_load_density": self.room_fire_load_density,
            "calorific_value": self.room_calorific_value_fire_load,
            "temperature_C": self.room_temp_inside_C,
            "temperature_K": self.temp_inside_K
        }