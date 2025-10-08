from math import exp, pow
from typing import Literal

from Room import Room
from Corridor import Corridor
from Level import Level

CALORIFIC_VALUE_WOOD = 13.8  # Низшая теплота сгорания древесины, МДж/кг

class Corridor_calculation():
    """
    


    Ограничения:
    - одна дверь - проем;
    - расчет через плотность пожарной нагрузки (расчет плотности надо реализовать отдельно);
    """
    def __init__(self,
                level: Level,
                room: Room,
                corridor: Corridor,
                building_type = Literal['жилое', 'общественное'],
                ):
        self.number = f"{level.number}-{corridor.corridor_number}-{room.room_number}"
        self.served_room = room
        self.served_corridor = corridor
        
        # Параметры проема
        self.opening1_area = self.served_corridor.corridor_opening1_area
        self.A0 = self.calc_A0(self.served_corridor)
        self.Fw = self.calc_Fw(room=self.served_room)
        # Проемность помещения
        self.room_opening_rate = self.calc_room_opening_rate(self.served_room, self.served_corridor.corridor_door_height_m)  
        
        # Параметры пожарной нагрузки
        self.Fw_unit_fire_load_by_walling = self.calc_Fw_unit_fire_load_by_walling(self.served_room)
        self.v0_air_for_burn = self.calc_v0_air_for_burn(self.served_room)
        self.unit_fire_load_critical = self.calc_unit_fire_load_critical(self.served_room)
        self.unit_fire_load_by_floor_square = self.calc_unit_fire_load_by_floor_square(self.served_room)

        # Параметры пожара
        self.fire_type = self.define_type_of_fire()
        self.max_temp = self.calc_max_temp(room=self.served_room)  # Максимальная температура в помещении (K)
        self.temp_smoke_coridor = self.calc_temp_smoke_coridor()  # Температура дыма в коридоре (K)
        
        self.corridor_smoke_hight_limit = self.calc_corridor_smoke_hight_limit(self.served_corridor)
        self.corridor_smoke_temp = self.calc_corridor_smoke_temp(corridor=self.served_corridor)
        self.corridor_door_area_m2 =  self.served_corridor.corridor_door_width_m * self.served_corridor.corridor_door_height_m
        
        self.coef_building_type = 1.0 if building_type == 'жилое' else 1.2
        self.smoke_consumption_mass_kg_s = self.calc_smoke_consumption_mass_kg_s(corridor=self.served_corridor)
        self.smoke_density = self.calc_smoke_density()
        self.smoke_consumption_vol = self.calc_smoke_consumption_vol_m3_h()


    def calc_Fw(self, room:Room) -> float:
        """
        Calculates the total area of internal surfaces of enclosing building structures (methodic-addition1_page51).
        Args:
            room (Room): Room object containing volume data
        Returns:
            float: Total surface area (m²)
        """
        return round(6 * pow(room.room_volume_m3, 0.667), 2)


    def calc_A0(self, corridor:Corridor) -> float:
        """
        Calculates the total area of room openings (methodic-addition1_page51).
        Args:
            corridor (Corridor): Corridor object containing opening data
        Returns:
            float: Total opening area (m²)
        """
        return corridor.corridor_opening1_area
    

    def calc_room_opening_rate(self, room:Room, hight_opening: float) -> float:
        """
        Calculates the opening rate of the room (methodic-addition1_page51).
        Args:
            room (Room): Room object
            height_opening (float): Opening height (m)
        Returns:
            float: Opening rate (m^0.5)
        """
        return round(self.A0 * pow(hight_opening, 0.5) / pow(room.room_volume_m3, 0.66), 3)


    def calc_Fw_unit_fire_load_by_walling(self, room:Room) -> float:
        """
        Calculates the specific fire load referred to the heat-receiving surface area of enclosing structures (methodic-addition1_page51).
        Args:
            room (Room): Room object with fire load data
        Returns:
            float: Specific fire load (kg/m²)
        """
        return round((room.room_area_m2 * room.room_fire_load_density) / (
                                                    (self.Fw - self.A0) * CALORIFIC_VALUE_WOOD), 2)
        
    def calc_v0_air_for_burn(self, room:Room) -> float:
        """
        Calculates the specific air volume required for complete combustion of the fire load (methodic-addition1_page52).
        Args:
            room (Room): Room object with calorific value data
        Returns:
            float: Air volume per kg of fire load (m³/kg)
        """
        
        # для расчета при списке пожарных нагрузок со списком масс
        # i = 0
        # for f, b in zip(self.room_calorific_value_fire_load, self.calorific_value_fire_load_mass):
        #     i += b * f/sum(self.calorific_value_fire_load_mass)

        # self.v0_air_for_burn = round((0.263 * i ), 2)

        return round(0.263 * room.room_calorific_value_fire_load, 2)

        
    def calc_unit_fire_load_critical(self, room:Room) -> float:
        """
        Calculates the critical specific fire load (methodic-addition1_page52).
        Args:
            room (Room): Room object with volume and air consumption data
        Returns:
            float: Critical fire load (kg/m²)
        """
        return round(((4500 * self.room_opening_rate ** 3) /(1 + (500 * self.room_opening_rate ** 3))) + \
                            ((room.room_volume_m3 ** 0.33) / (6 * self.v0_air_for_burn)), 3)


    def calc_unit_fire_load_by_floor_square(self, room:Room) -> float:
        """
        Calculates the specific fire load referred to the floor area.
        Args:
            room (Room): Room object with fire load density
        Returns:
            float: Fire load per m² of floor area (kg/m²)
        """
        return round(room.room_fire_load_density / CALORIFIC_VALUE_WOOD, 3)


    def define_type_of_fire(self) -> str:
        """
        Determines the type of fire based on fire load and ventilation conditions (methodic-page14).
        
        Returns:
            str: Fire type ('FIRE_BY_VENT' or 'FIRE_BY_FIRELOAD')
        """
        if (self.Fw_unit_fire_load_by_walling > self.unit_fire_load_critical):
            return 'FIRE_BY_VENT'
        else:
            return 'FIRE_BY_FIRELOAD'

    def calc_max_temp(self, room:Room) -> float:
        """
        Calculates the maximum average temperature in the room (methodic-page14).
        Args:
            room (Room): Room object with initial temperature
        Returns:
            float: Maximum temperature (K)
        """
        if self.fire_type == 'FIRE_BY_VENT':
            return round(room.temp_inside_K + 940 * exp(0.0047 * self.unit_fire_load_by_floor_square - 0.141), 3)
        else:
            return round(room.temp_inside_K + 224 * pow(self.Fw_unit_fire_load_by_walling, 0.528), 3)

    def calc_temp_smoke_coridor(self) -> float:
        """
        Calculates the smoke temperature flows from room to the corridor (methodic-page15).
        Returns:
            float: Smoke temperature (K)
        """
        return round(0.8 * self.max_temp, 2)

    def calc_corridor_smoke_hight_limit(self, corrifor:Corridor, h=0.55) -> float:
        """
        Calculates the limiting smoke height in the corridor (methodic-page16).
        Args:
            corrifor (Corridor): Corridor object with height data
            h (float, optional): Proportion coefficient. Defaults to 0.55.
        Returns:
            float: Limiting smoke height (m)
        """
        return round(corrifor.corridor_height_m * h, 3)
    
    def calc_corridor_smoke_temp(self, corridor:Corridor) -> float:
        """
        Calculates the temperature of smoke in the corridor (methodic-page15).
        Args:
            corridor (Corridor): Corridor object
        Returns:
            float: Smoke temperature (K)
        """
        a = corridor.corridor_temp_K

        b = (1.22 * (self.temp_smoke_coridor - corridor.corridor_temp_K) *
             (2 * self.corridor_smoke_hight_limit + (corridor.corridor_area_m2 / corridor.corridor_length_m))) / corridor.corridor_length_m
        
        c = 1 - exp((-0.58 * corridor.corridor_length_m) / (2 * self.corridor_smoke_hight_limit + (corridor.corridor_area_m2 / corridor.corridor_length_m)))

        return round(a + b * c, 2)

    def calc_smoke_consumption_mass_kg_s(self, corridor:Corridor) -> float:
        """
        Calculates the mass flow rate of smoke.
        Args:
            corridor (Corridor): Corridor object
        Returns:
            float: Mass flow rate (kg/s)
        """
        return round(self.coef_building_type * self.corridor_door_area_m2 * pow(corridor.corridor_door_height_m, 0.5), 3)

    def calc_smoke_density(self) -> float:
        """
        Calculates the density of smoke.
        Returns:
            float: Smoke density (kg/m³)
        """
        return round(353 / self.corridor_smoke_temp, 2)

    def calc_smoke_consumption_vol_m3_h(self) -> float:
        """
        Calculates the volumetric flow rate of smoke.
        Returns:
            float: Volumetric flow rate (m³/h)
        """
        return round(3600 * (self.smoke_consumption_mass_kg_s / self.smoke_density), 3)

    def to_dict(self) -> dict:
            """
            Returns:
                dict: Dictionary containing all calculated parameters
            """
            return {
                "room": self.served_room.to_dict(),
                "corridor": self.served_corridor.to_dict(),
                "building_type": "жилое" if self.coef_building_type == 1.0 else "общественное",
                "opening1_area": self.opening1_area,
                "A0": self.A0,
                "Fw": self.Fw,
                "room_opening_rate": self.room_opening_rate,
                "Fw_unit_fire_load_by_walling": self.Fw_unit_fire_load_by_walling,
                "v0_air_for_burn": self.v0_air_for_burn,
                "unit_fire_load_critical": self.unit_fire_load_critical,
                "unit_fire_load_by_floor_square": self.unit_fire_load_by_floor_square,
                "fire_type": self.fire_type,
                "max_temp": self.max_temp,
                "temp_smoke_room_to_coridor": self.temp_smoke_coridor,
                "corridor_smoke_hight_limit": self.corridor_smoke_hight_limit,
                "corridor_smoke_temp": self.corridor_smoke_temp,
                "corridor_door_area_m2": self.corridor_door_area_m2,
                "coef_building_type": self.coef_building_type,
                "smoke_consumption_mass_kg_s": self.smoke_consumption_mass_kg_s,
                "smoke_density": self.smoke_density,
                "smoke_consumption_vol": self.smoke_consumption_vol,
            }