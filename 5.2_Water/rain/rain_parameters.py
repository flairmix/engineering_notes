from pydantic import BaseModel
from typing import Dict, Optional

from enum import Enum

class PValue(Enum):
    P_1_3 = 0.33
    P_1_2 = 0.5
    P_1 = 1
    P_2 = 2
    P_5 = 5
    P_10 = 10
    P_20 = 20
    P_50 = 50

# p_value_item = PValue.P_1
# dict_rain_q20[p_value_item.name]['Москва']

# dict_rain_type['district']['Москва']
# dict_rain_coeff_c['coeff_c']['Москва']
# dict_rain_layer_h_a['ha']['Москва']



class RainfallParams(BaseModel):
    """
    Parameters for calculating rainfall runoff (Q_r) according to formula (Ж.1).
    
    Formula: Q_r = (Z_mid * A^1.2 * F_r) / (t_r^(1.2n - 0.1))

    - Z_{mid}: average surface coefficient (from tables Ж.6 and Ж.7)
    - A: design rainfall intensity parameter (from formula Ж.2)
    - F_r: design runoff area (ha), ≤ 150 ha
    - t_r: design rainfall duration (s)
    - n: exponent value (from table Ж.1)
    """
    Z_mid: float
    A: float
    F_r: float
    t_r: float
    n: float

    def calculate_Q_r(self) -> float:
        """
        Calculate rainfall runoff Q_r in L/s.

        Returns:
            Q_r (float)
        """
        numerator = self.Z_mid * (self.A ** 1.2) * self.F_r
        denominator = self.t_r ** (1.2 * self.n - 0.1)
        Q_r = numerator / denominator
        return round(Q_r, 4)



class IntensityParams(BaseModel):
    """
    Parameters for calculating intensity parameter A according to formula (Ж.2).
    
    Formula: A = q_20 * 20^n * (1 + lg(P)/lg(m_r))^y

    Where:
        - q_{20}: rainfall intensity (20 min, P=1 year) — from figure Ж.1
        - n: exponent value (from table Ж.1)
        - P: return period (years)
        - m_r: average number of rainfalls per year (from table Ж.1)
        - y: exponent value
    """
    q_20: float = 91.0
    n: float = 0.71
    P: float = 1.0
    m_r: float = 150.0
    y: float = 1.54

    def calculate_A(self) -> float:
        """
        Calculate parameter A for rainfall runoff calculation.

        Returns:
            A (float)
        """
        import math
        lg_P = math.log10(self.P)
        lg_m_r = math.log10(self.m_r)
        A = round(self.q_20 * (20 ** self.n) * (1 + (lg_P / lg_m_r)) ** self.y, 3)
        return A



class WeightedAverageParams(BaseModel):
    """
    Parameters for calculating weighted average coefficient Z_mid based on surface areas.
    
    Formula: Z_mid = Σ(coefficient_i × area_i) / Σ(area_i)

    If total area is 0, returns 0.0 (to avoid division by zero).
    """
    coefficients_dict: Dict[str, float] = {
        "Waterproof surfaces": 0.33,
        "Paving stones and crushed stone pavements": 0.297,
        "Cobblestone pavements": 0.145,
        "Crushed stone coatings not treated with binders": 0.125,
        "Gravel garden and park paths": 0.09,
        "Unpaved surfaces (planned)": 0.064,
        "Lawns": 0.038,
    }

    areas_dict: Dict[str, float] = {
        "Waterproof surfaces": 1.0,
        "Paving stones and crushed stone pavements": 0.0,
        "Cobblestone pavements": 0.0,
        "Crushed stone coatings not treated with binders": 0.0,
        "Gravel garden and park paths": 0.0,
        "Unpaved surfaces (planned)": 0.0,
        "Lawns": 0.0,
    }

    def calculate_Z_mid(self) -> float:
        """
        Compute weighted average surface coefficient Z_mid.

        Returns:
            Z_mid (float): Rounded to 3 decimal places.
                           Returns 0.0 if total area is zero.
        """
        total_weighted_sum = 0.0
        total_area = 0.0

        for cover_type, area in self.areas_dict.items():
            if cover_type not in self.coefficients_dict:
                raise KeyError(f"Surface type '{cover_type}' not found in coefficients_dict.")
            if area < 0:
                raise ValueError(f"Area for '{cover_type}' is negative: {area}")

            coefficient = self.coefficients_dict[cover_type]
            total_weighted_sum += coefficient * area
            total_area += area

        if total_area == 0:
            return 0.0

        weighted_average = total_weighted_sum / total_area
        return round(weighted_average, 3)


class DurationRainFlowOnSurfaceAndPipes(BaseModel):
    """

    """
    t_con: float = 5.0
    t_can: float = 0
    t_p: float = 0

    l_v_can_segments_length_velocity: dict[float, float] = {0, 0}
    l_v_p_segments_length_velocity: dict[float, float] = {100, 1.0}

    # tcon - продолжительность протекания дождевых вод до уличного лотка или при наличии дождеприемников 
    # в пределах квартала до уличного коллектора (время поверхностной концентрации), мин, определяется согласно Ж.6;
    # Ж.6 Время поверхностной концентрации дождевого стока tcon следует рассчитывать или, 
    # при отсутствии внутриквартальных закрытых дождевых сетей в поселениях и городских округах, принимать 
    # 5 - 10 мин, а при их наличии - 3 - 5 мин. 
    # При расчете внутриквартальной канализационной сети время поверхностной концентрации следует принимать 2 - 3 мин.

    def calculate_t_r(self) -> float:
        # Продолжительность протекания дождевых вод по уличным лоткам tcan следует определять по формуле Ж.4
        # где lcan - длина участков лотков, м;
        # lcan - расчетная скорость течения на участке, м/с.
        for l, v in self.l_v_can_segments_length_velocity.items():
            t_can += l/v
        t_can *= 0.021
        
        # Продолжительность протекания дождевых вод по трубам до рассчитываемого сечения tр, мин, следует определять по формуле Ж.5
        # где lр - длина расчетных участков коллектора, м;
        # vр - расчетная скорость течения на участке, м/с.
        for l, v in self.l_v_p_segments_length_velocity.items():
            t_p += l/v
        t_p *= 0.017

        # Ж.5 Расчетную продолжительность протекания дождевых вод по поверхности и трубам до расчетного участка (створа) tr, мин, следует определять по формул
        t_r = round(self.t_con + t_can + t_p, 3)

        return t_r


















    def calculate_Q_r(self) -> float:
        """
        Calculate rainfall runoff Q_r in L/s.

        Returns:
            Q_r (float)
        """
        numerator = self.Z_mid * (self.A ** 1.2) * self.F_r
        denominator = self.t_r ** (1.2 * self.n - 0.1)
        Q_r = numerator / denominator
        return round(Q_r, 4)
