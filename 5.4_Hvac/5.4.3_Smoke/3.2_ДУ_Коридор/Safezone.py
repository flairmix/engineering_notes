from typing import Literal
import math

class Safezone:
    def __init__(self,
                location_type: Literal['above-ground', 'underground'] = 'above-ground',
                door_square_m2 = 3.0,
                air_velocity_regulated_m_s = 1.5,
                density_air=(353/(273-26)),
                ):
        
        self.location_type = location_type
        self.door_square_m2 = door_square_m2
        self.air_velocity_regulated_m_s = air_velocity_regulated_m_s
        self.density_air = density_air





    def G_safezone_heat_m3_h(self,
                             n, 
                             Fd, 
                             m, 
                             Fdl, 
                             Sdl=(2600/1.21), 
                             Sd=5300/(353/(273+18)),
                             ) -> int:
        '''
        n - количество дверей
        Fd - площадь двери
        Sd - характеристика удельного сопротивления дверей 
        m - количество дверей лифтов без подпора
        Fdl - площадь двери лифта без подпора
        Sdl - характеристика удельного сопротивления дверей лифта
        '''
        return round((((n * Fd * math.sqrt(20/Sd))) + (m * Fdl * math.sqrt(20/Sdl))) * 3600 / (353/(273+18)))