
class Corridor:
    def __init__(self,
                corridor_number: str,
                corridor_height_m: float,
                corridor_door_height_m: float,
                corridor_door_width_m: float,
                corridor_area_m2: float,
                corridor_length_m: float,
                corridor_coef_building_type: float,
                corridor_temp_C: float):
        
        # Основные параметры коридора
        self.corridor_number = corridor_number
        self.corridor_height_m = corridor_height_m
        self.corridor_door_height_m = corridor_door_height_m
        self.corridor_door_width_m = corridor_door_width_m
        self.corridor_area_m2 = corridor_area_m2
        self.corridor_length_m = corridor_length_m
        self.corridor_coef_building_type = corridor_coef_building_type
        self.corridor_temp_C = corridor_temp_C
        self.corridor_temp_K = corridor_temp_C + 273.15
        
        # Вычисляемые параметры
        self.corridor_opening1_area = self.corridor_door_height_m * self.corridor_door_width_m

    def __str__(self):
        """
        Возвращает строковое представление объекта Corridor
        """
        return (f"Коридор: {self.corridor_number}\n"
                f"Высота: {self.corridor_height_m} м\n"
                f"Площадь: {self.corridor_area_m2} м²\n"
                f"Длина: {self.corridor_length_m} м\n"
                f"Температура: {self.corridor_temp_C} °C ({self.corridor_temp_K} K)")
    
    def to_dict(self) -> dict:
        """
        Возвращает все параметры коридора в виде словаря
        """
        return {
            "corridor_number": self.corridor_number,
            "height_m": self.corridor_height_m,
            "door_height_m": self.corridor_door_height_m,
            "door_width_m": self.corridor_door_width_m,
            "area_m2": self.corridor_area_m2,
            "length_m": self.corridor_length_m,
            "building_type_coef": self.corridor_coef_building_type,
            "temperature_C": self.corridor_temp_C,
            "temperature_K": self.corridor_temp_K,
            "opening_area_m2": self.corridor_opening1_area
            }


