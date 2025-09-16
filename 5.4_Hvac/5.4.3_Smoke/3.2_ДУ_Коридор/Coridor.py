class Corridor:
    """
    Класс для представления характеристик коридора в здании.
    
    Параметры:
    - corridor_system_name: название системы коридора
    - corridor_level: уровень расположения коридора (этаж)
    - corridor_height_m: высота коридора (в метрах)
    - corridor_door_height_m: высота дверного проема (в метрах)
    - corridor_door_width_m: ширина дверного проема (в метрах)
    - corridor_area_m2: площадь коридора (в квадратных метрах)
    - corridor_length_m: длина коридора (в метрах)
    - corridor_coef_building_type: коэффициент типа здания
    - corridor_temp: температура в коридоре (в градусах Цельсия)
    """
    
    def __init__(self,
                corridor_system_name: str,
                corridor_level: int,
                corridor_height_m: float,
                corridor_door_height_m: float,
                corridor_door_width_m: float,
                corridor_area_m2: float,
                corridor_length_m: float,
                corridor_coef_building_type: float,
                corridor_temp: float):
        
        # Основные параметры коридора
        self.corridor_system_name = corridor_system_name
        self.corridor_level = corridor_level
        self.corridor_height_m = corridor_height_m
        self.corridor_door_height_m = corridor_door_height_m
        self.corridor_door_width_m = corridor_door_width_m
        self.corridor_area_m2 = corridor_area_m2
        self.corridor_length_m = corridor_length_m
        self.corridor_coef_building_type = corridor_coef_building_type
        self.corridor_temp = corridor_temp
        
        # Вычисляемые параметры
        self.corridor_opening1_area = self.corridor_door_height_m * self.corridor_door_width_m
        self.corridor_temp_K = self.corridor_temp + 273.15  # Преобразование в Кельвины

    def __str__(self):
        """
        Возвращает строковое представление объекта Corridor
        """
        return (f"Коридор: {self.corridor_system_name}\n"
                f"Уровень: {self.corridor_level}\n"
                f"Высота: {self.corridor_height_m} м\n"
                f"Площадь: {self.corridor_area_m2} м²\n"
                f"Длина: {self.corridor_length_m} м\n"
                f"Температура: {self.corridor_temp} °C ({self.corridor_temp_K} K)")

    def get_door_parameters(self):
        """
        Возвращает параметры дверного проема
        """
        return {
            "высота": self.corridor_door_height_m,
            "ширина": self.corridor_door_width_m,
            "площадь": self.corridor_opening1_area
        }

    def get_basic_info(self):
        """
        Возвращает основную информацию о коридоре
        """
        return {
            "название": self.corridor_system_name,
            "уровень": self.corridor_level,
            "площадь": self.corridor_area_m2,
            "длина": self.corridor_length_m
        }
