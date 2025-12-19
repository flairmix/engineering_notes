import math
from dataclasses import dataclass

@dataclass
class EmissionData:
    vehicle_type: str  # Тип автомобиля
    q_i_co_emission_g_km: float  # Удельный выброс CO, г/км
    q_i_ch_emission_g_km: float  # Удельный выброс CH, г/км
    q_i_nox_emission_g_km: float  # Удельный выброс NOx, г/км
    q_i_so2_emission_g_km: float  # Удельный выброс SO2, г/км

avg_car = EmissionData(
    vehicle_type="авт. среднего класса",
    q_i_co_emission_g_km=20.8,
    q_i_ch_emission_g_km=1.3,
    q_i_nox_emission_g_km=0.63,
    q_i_so2_emission_g_km=0.09
)

small_truck_petrol = EmissionData(
    vehicle_type="грузовые авт. мал. класса, бензиновые",
    q_i_co_emission_g_km=59.5,
    q_i_ch_emission_g_km=7.2,
    q_i_nox_emission_g_km=2.2,
    q_i_so2_emission_g_km=0.13
)

small_truck_diesel = EmissionData(
    vehicle_type="грузовых авт. мал. класса, дизельные",
    q_i_co_emission_g_km=32.6,
    q_i_ch_emission_g_km=10.3,
    q_i_nox_emission_g_km=6.9,
    q_i_so2_emission_g_km=0.85
)

def calculate_emission_mass(q_i, 
                            L, 
                            A_Э_TO_i, 
                            K_C, 
                            t_B_TO,
                            ):
    """
    Calculates the mass of emission of the j-th pollutant (Mj) in grams per second (g/s).
    
    Parameters:
    - q_i (float): specific emission rate of the j-th pollutant per one vehicle of the i-th type, g/km.
    - L (float): estimated mileage of one vehicle per cycle on the enterprise premises (including engine start, movement, and time at maintenance zones), km.
    - A_Э_TO_i (float): operational number of vehicles at parking lots, accounting for the dispatch coefficient (number of vehicles entering the maintenance zone).
    - K_C (float): coefficient reflecting the impact of vehicle speed (driving mode).
    - t_B_TO (float): time for vehicle dispatch or return (entering maintenance), in hours.
    
    Returns:
    - Mj (float): mass of the j-th pollutant emission, g/s.
    """
    Mj = 10**-3 * (q_i * L * A_Э_TO_i * K_C) / (t_B_TO * 3.6)
    return Mj


def calculate_total_emission_mass(q_list, 
                                  L, 
                                  A_Э_TO_list, 
                                  K_C_list, 
                                  t_B_TO,
                                  ):
    """
    Calculates the total mass of emissions for multiple vehicle types (n types).
    
    Parameters:
    - q_list (list): list of specific emission rates for each vehicle type, g/km.
    - L (float): estimated mileage per cycle (same for all vehicle types), km.
    - A_Э_TO_list (list): list of operational numbers of vehicles for each type.
    - K_C_list (list): list of driving mode coefficients for each vehicle type.
    - t_B_TO (float): dispatch/return time for vehicles (same for all types), hours.
    
    Returns:
    - total_Mj (float): total mass of pollutant emissions from all vehicle types, g/s.
    """
    total_Mj = 0
    for i in range(len(q_list)):
        Mj = calculate_emission_mass(q_list[i], L, A_Э_TO_list[i], K_C_list[i], t_B_TO)
        total_Mj += Mj
    return total_Mj



def calc(
        parking_places: int,
         ):
    """
    2.1. Воздухообмен в гаражах-стоянках индивидуального (личного) транспорта определяется расчетом при усредненном значении количества
    въездов и выездов соответственно равным 2 и 8% от общего количества машино-мест. При этом концентрация оксида углерода (CO) следует
    принимать 20 (мг/куб. м). Значение воздухообмена не должно составлять менее 150 (куб. м/час) на одно машиноместо.
    """
    auto_move_in = math.ceil(parking_places * 0.02)
    auto_move_out = math.ceil(parking_places * 0.08)

    return 0