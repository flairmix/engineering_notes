from smoke_const import CALORIFIC_VALUE_WOOD
from .Room import Room
from Corridor import Corridor


def corridor_calc_one(room: Room, corridor: Corridor) -> list:
    """
    Calculation smoke exhaust parameters for pair: Room - Corridor.
    Results writes in Room instance.
    Parameters for output returns as List.
    """
    room.calc_Fw()
    room.get_opening1_area(corridor.corridor_opening1_area)
    room.calc_A0()
    room.calc_Fw_unit_fire_load_by_walling()
    room.calc_v0_air_for_burn()
    room.calc_room_opening_rate(corridor.corridor_door_height_m)
    room.calc_unit_fire_load_critical()
    room.calc_unit_fire_load_by_floor_square()
    room.define_type_of_fire()
    room.get_corridor_temp(corridor.corridor_temp)
    room.calc_max_temp()
    room.calc_temp_smoke_coridor()
    room.get_corridor_hight(corridor.corridor_height_m)
    room.get_corridor_door_hight(corridor.corridor_door_height_m)
    room.get_corridor_door_width(corridor.corridor_door_width_m)
    room.get_corridor_area(corridor.corridor_area_m2)
    room.get_corridor_lenght(corridor.corridor_length_m)
    room.calc_corridor_smoke_hight_limit()
    room.calc_corridor_smoke_temp()
    room.calc_corridor_door_area()
    room.get_coef_building_type(corridor.corridor_coef_building_type)
    room.calc_smoke_consumption_mass()
    room.calc_smoke_density()
    room.calc_smoke_consumption_vol()

    parameter =  [
        "-",
        room.room_name,
        room.room_area_m2,
        room.room_high_m,
        room.room_volume_m3,
        room.Fw,
        room.corridor_door_width,
        room.corridor_door_hight,
        room.A0,
        CALORIFIC_VALUE_WOOD,
        room.room_fire_load_density,
        room.Fw_unit_fire_load_by_walling,
        room.room_calorific_value_fire_load,
        room.v0_air_for_burn,
        room.room_opening_rate,
        room.unit_fire_load_critical,
        room.unit_fire_load_by_floor_square,
        "Регулируемый вентиляцией" if room.fire_type.value == 1 else "Регулируемый нагрузкой",
        room.room_temp_inside,
        room.room_temp_inside + 273,
        room.max_temp,
        room.temp_smoke_coridor,
        room.corridor_hight,
        room.corridor_area,
        room.corridor_lenght,
        room.corridor_smoke_hight_limit,
        room.corridor_temp_K - 273,
        room.corridor_temp_K,
        room.corridor_smoke_temp,
        room.coef_building_type,
        room.corridor_door_hight,
        room.corridor_door_width,
        room.corridor_door_area,
        room.smoke_consumption_mass,
        room.smoke_density,
        room.smoke_consumption_vol
    ]

    for i in range(0, len(parameter)):
        if type(parameter[i]) == float:
            parameter[i] = round(parameter[i], 2)
            
    return parameter