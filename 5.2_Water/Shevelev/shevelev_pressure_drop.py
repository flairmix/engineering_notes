from typing import Literal
from pydantic import validate_call

g = 9.81

@validate_call
def calculate_shevelev_pressure_drop(
    pipe_type: Literal["steel_new", "cast_iron_new", "steel_used", "cast_iron_used"],
    diameter_mm: float,  # диаметр трубы, мм
    flow_rate_l_s: float  # расход, л/с
) -> dict[str, float]:
    """
    Расчет потерь давления по методу Шевелева
    
    Args:
        pipe_type: тип трубы
        diameter_mm: диаметр трубы в мм
        flow_rate_l_s: расход в л/с
        
    Returns:
        dict с результатами расчета: скорость и потери напора
    """
    # Расчет скорости потока
    velocity = round(10**6 * ((flow_rate_l_s * 3.6) / (diameter_mm**2) / 2826), 2)
    
    if pipe_type in ("steel_new", "cast_iron_new"):
        if velocity >= 1.2:
            # формула #6 - книга Шевелева
            i_1000 = round(1000 * 0.00107 * (velocity**2 / (diameter_mm/1000) ** 1.3), 3)
        else:
            # формула #7 - книга Шевелева
            i_1000 = round(1000 * 0.000912 * 
                          ((velocity**2) / ((diameter_mm/1000) ** 1.3)) * 
                          pow(1 + (0.867/velocity), 0.3), 3)
    
    elif pipe_type in ("steel_used", "cast_iron_used"):
        # формула #5a - книга Шевелева
        _lambda = (0.0179/(pow(diameter_mm/1000, 0.3))) * pow(1 + (0.867/velocity), 0.3)
        # формула #1 - книга Шевелева
        i_1000 = round(1000 * _lambda * 
                      (1/(diameter_mm/1000)) * 
                      (velocity**2 / (2*g)), 3)
    
    else:
        raise ValueError("Неверный тип трубы")
    
    # Расчет давления в Па (1 мм вод.ст. = 9.80665 Па)
    pressure_pa = round(i_1000 * 9.80665, 2)
    
    return {
        "velocity_m_s": velocity,
        "pressure_loss_mm_m": i_1000,
        "pressure_loss_Pa": pressure_pa,
    }
