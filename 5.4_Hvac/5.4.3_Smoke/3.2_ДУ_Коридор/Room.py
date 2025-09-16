from enum import Enum
from math import exp, pow

# Константы
CALORIFIC_VALUE_WOOD = 13.8  # Низшая теплота сгорания древесины, МДж/кг

class FireType(Enum):
    """Типы объемного пожара"""
    FIRE_BY_VENT = 1  # Пожар по вентиляции
    FIRE_BY_FIRELOAD = 2  # Пожар по пожарной нагрузке

class Room:
    """
    Класс для представления характеристик помещения при пожаре
    
    Основные параметры:
    - room_systemname: системное имя помещения
    - room_name: название помещения
    - room_level: уровень расположения помещения (этаж)
    - room_area_m2: площадь помещения (м²)
    - room_high_m: высота помещения (м)
    - room_fire_load_density: плотность пожарной нагрузки (кг/м²)
    - room_calorific_value_fire_load: теплота сгорания пожарной нагрузки (МДж/кг)
    - room_temp_inside: начальная температура воздуха (°C)
    """
    
    def __init__(self,
                 room_systemname: str,
                 room_name: str,
                 room_level: int,
                 room_area_m2: float,
                 room_high_m: float,
                 room_fire_load_density: float,
                 room_calorific_value_fire_load: float,
                 room_temp_inside: int = 24):
        
        # Основные параметры помещения
        self.room_systemname = room_systemname
        self.room_name = room_name
        self.room_level = room_level
        self.room_area_m2 = room_area_m2
        self.room_high_m = room_high_m
        self.room_volume_m3 = room_area_m2 * room_high_m
        self.room_fire_load_density = room_fire_load_density
        self.room_calorific_value_fire_load = room_calorific_value_fire_load
        self.room_temp_inside = room_temp_inside
        self.temp_inside_K = room_temp_inside + 273
        
        # Параметры пожара
        self.fire_type = FireType.FIRE_BY_VENT
        self.max_temp = 0  # Максимальная температура в помещении (K)
        self.temp_smoke_coridor = 0  # Температура дыма в коридоре (K)
        
        # Параметры проема
        self.opening1_area = 0
        self.A0 = 0
        self.Fw = 0  # Суммарная площадь поверхности конструкций
        self.room_opening_rate = 0  # Проемность помещения
        
        # Параметры пожарной нагрузки
        self.Fw_unit_fire_load_by_walling = 0
        self.unit_fire_load_critical = 0
        self.unit_fire_load_by_floor_square = 0
        self.v0_air_for_burn = 0
        
        # Параметры коридора
        self.corridor_hight = 0
        self.corridor_door_hight = 0
        self.corridor_door_width = 0
        self.corridor_area = 0
        self.corridor_lenght = 0
        self.corridor_smoke_hight_limit = 0
        self.corridor_temp = 0
        self.corridor_temp_K = 0
        self.corridor_smoke_temp = 0
        self.corridor_door_area = 0
        
        # Дополнительные параметры
        self.coef_building_type = 1.2
        self.smoke_consumption_mass = 0
        self.smoke_density = 0
        self.smoke_consumption_vol = 0

    
    def __str__(self):
        return f"class Room: id-{self.id}, system - {self.room_systemname}, room_name - {self.room_name}"

    def calc_Fw(self) -> None:
        """
        Суммарная площадь внутренней поверхности ограждающих строительных конструкций
        Приложение 1 МР 2013
        """
        self.Fw = round(6 * pow(self.room_volume_m3, 0.667), 2)

    def get_opening1_area(self, opening1_area) -> None:
        self.opening1_area = opening1_area

    def calc_A0(self) -> None:
        """
        Суммарная площадь проемов помещения
        Приложение 1 МР 2013. 
        Ai - площадь i-го проема
        """
        self.A0 = self.opening1_area

    # def get_fire_load_density(self, room_fire_load_density: int)-> None:
    #     """
    #     Плотность пожарной нагрузки помещения
    #     q_п
    #     СИТИС-СПН-1. Пожарная нагрузка. Справочник (Таблица 1)
    #     """
    #     self.room_fire_load_density = room_fire_load_density

    def calc_Fw_unit_fire_load_by_walling(self) -> None:
        """
        2. gk - удельная приведенная пожарная нагрузка, отнесенная к площади тепловоспринимающей поверхности
        ограждающих строительных конструкций, кг/м2
        Приложение 1 МР 2013
        """
        self.Fw_unit_fire_load_by_walling = round((self.room_area_m2 * self.room_fire_load_density) / (
                                                    (self.Fw - self.A0) * CALORIFIC_VALUE_WOOD), 2)

    # def get_calorific_value_fire_load(self, room_calorific_value_fire_load: float):
    #     """
    #     Средняя теплота сгорания пожарной нагрузки МДж/кг
    #     Приложение 1 МР 2013. А также: СИТИС-СПН-1. Пожарная нагрузка. Справочник (Таблица 2)
    #     """
    #     self.room_calorific_value_fire_load = room_calorific_value_fire_load

    def calc_v0_air_for_burn(self) -> None:
        """
        V0 - Удельное количество воздуха, необходимое для полного сгорания пожарной нагрузки помещения, 
        м3/кг
        Приложение 1 МР 2013
        """
        # для расчета при списке пожарных нагрузок со списком масс
        # i = 0
        # for f, b in zip(self.room_calorific_value_fire_load, self.calorific_value_fire_load_mass):
        #     i += b * f/sum(self.calorific_value_fire_load_mass)

        # self.v0_air_for_burn = round((0.263 * i ), 2)

        self.v0_air_for_burn = round(0.263 * self.room_calorific_value_fire_load, 2)

    def calc_room_opening_rate(self, hight_opening: float) -> None:
        """
        П - Проемность помещения, pow(м, 0.5)
        """
        self.room_opening_rate = round(self.A0 * pow(hight_opening, 0.5) / pow(self.room_volume_m3, 0.66), 3)

    def calc_unit_fire_load_critical(self) -> None:
        """
        Удельное критическое количество пожарной нагрузки
        кг/м2
        Приложение 1 МР 2013
        """
        self.unit_fire_load_critical = (
                                               (4500 * self.room_opening_rate ** 3) /
                                               (1 + (500 * self.room_opening_rate ** 3))) + (
                                               (self.room_volume_m3 ** 0.33) / (6 * self.v0_air_for_burn))

    def calc_unit_fire_load_by_floor_square(self) -> None:
        """
        Удельная приведенная пожарная нагрузка, отнесенная к площади пола помещения
        кг/м2
        Приложение 1 МР 2013
        """
        self.unit_fire_load_by_floor_square = self.room_fire_load_density / CALORIFIC_VALUE_WOOD

    def define_type_of_fire(self) -> None:
        """
        Вид объемного пожара
        gk > gkкр = ПРВ
        gk < gkкр = ПРН

        FIRE_BY_VENT = 1
        FIRE_BY_FIRELOAD = 2
        """
        self.fire_type.FIRE_BY_VENT if \
            self.Fw_unit_fire_load_by_walling > self.unit_fire_load_critical \
            else self.fire_type.FIRE_BY_FIRELOAD

    # def get_temp_inside(self, room_temp_inside : int) -> None:
    #     self.room_temp_inside = room_temp_inside

    # def get_temp_coridor(self, temp_smoke_coridor: int) -> None:
    #     self.temp_smoke_coridor = temp_smoke_coridor
    #     self.corridor_temp_K = temp_smoke_coridor + 273

    def calc_max_temp(self) -> None:
        """ Максимальная среднеобъемная температура в помещении K"""
        if self.fire_type == FireType.FIRE_BY_VENT:
            self.max_temp = self.temp_inside_K + 940 * exp(
                0.0047 * self.unit_fire_load_by_floor_square - 0.141)
        else:
            self.max_temp = self.temp_inside_K + 224 * pow(
                self.Fw_unit_fire_load_by_walling, 0.528)

    def calc_temp_smoke_coridor(self) -> None:
        """	Максимальная среднеобъемная температура в помещении"""
        self.temp_smoke_coridor = 0.8 * self.max_temp

    def get_corridor_hight(self, corridor_hight: float) -> None:
        self.corridor_hight = corridor_hight

    def get_corridor_door_hight(self, corridor_door_hight: float) -> None:
        self.corridor_door_hight = corridor_door_hight

    def get_corridor_door_width(self, corridor_door_width: float) -> None:
        self.corridor_door_width = corridor_door_width

    def get_corridor_area(self, corridor_area: float) -> None:
        self.corridor_area = corridor_area

    def get_corridor_lenght(self, corridor_lenght: float) -> None:
        self.corridor_lenght = corridor_lenght

    def calc_corridor_smoke_hight_limit(self, h=0.55):
        self.corridor_smoke_hight_limit = self.corridor_hight * h

    def get_corridor_temp(self, corridor_temp: float = 24) -> None:
        self.corridor_temp = corridor_temp
        self.corridor_temp_K = self.corridor_temp + 273

    def calc_corridor_smoke_temp(self) -> None:
        a = self.corridor_temp_K
        b = (1.22 * (self.temp_smoke_coridor - self.corridor_temp_K) *
             (2 * self.corridor_smoke_hight_limit +
              (self.corridor_area / self.corridor_lenght))
             ) / self.corridor_lenght
        c = 1 - exp((-0.58 * self.corridor_lenght) /
                    (2 * self.corridor_smoke_hight_limit +
                     (self.corridor_area / self.corridor_lenght)))

        self.corridor_smoke_temp = a + b * c

    def calc_corridor_door_area(self) -> None:
        self.corridor_door_area = self.corridor_door_width * self.corridor_door_hight

    def get_coef_building_type(self, coef_building_type: float = 1.2) -> None:
        self.coef_building_type = coef_building_type

    def calc_smoke_consumption_mass(self) -> None:
        self.smoke_consumption_mass = self.coef_building_type * self.corridor_door_area * pow(
            self.corridor_door_hight, 0.5)

    def calc_smoke_density(self) -> None:
        self.smoke_density = 353 / self.corridor_smoke_temp

    def calc_smoke_consumption_vol(self) -> None:
        self.smoke_consumption_vol = 3600 * (self.smoke_consumption_mass /
                                             self.smoke_density)