import math
from typing import Literal, List, Dict
import pandas as pd

class PipeSegment:
    def __init__(self, 
                 dn_m = Literal[20, 25, 38, 45, 57, 76, 89, 108, 133, 157, 219, 273, 325],
                 material = Literal['steel', 'plastic'], 
                 length_m=1, 
                 thickness_m: float = 0.025, 
                 isolation_lambda: float = 0.05, 
                 tin=65,
                 tout=18,
                 ):
        self.dn_m = dn_m
        self.material = material
        self.length_m = length_m
        self.thickness_m = thickness_m
        self.isolation_lambda = isolation_lambda
        self.isolation_d2 = dn_m + (2 * thickness_m)
        self.K = 1.2 if self.material == "steel" else 1.7
        self.alpha_is = 10
        self.tin = tin
        self.tout = tout
        self.q_L = round(self.heatloss_pipe_unit())
        self.Qloss_W = round(self.q_L * self.length_m)

    def heatloss_pipe_unit(self) -> float:
        Ris = ((1/(2*math.pi*self.isolation_lambda))) * math.log(self.isolation_d2/self.dn_m)
        
        Ris_L = 1 / (math.pi*self.isolation_d2*self.alpha_is)

        return self.K * (self.tin - self.tout) / (Ris + Ris_L)

    def to_dict(self):
        return {
            'DN (м)': self.dn_m,
            'Материал': self.material,
            'Длина (м)': self.length_m,
            'Толщина изоляции (м)': self.thickness_m,
            'Теплопроводность изоляции': self.isolation_lambda,
            'Температура внутри (°C)': self.tin,
            'Температура снаружи (°C)': self.tout,
            'Потери тепла (Вт/м)': self.q_L,
            'Общие потери тепла (Вт)': self.Qloss_W
        }

class PipeSystem:
    def __init__(self):
        self.segments: List[PipeSegment] = []

    def add_segment(self, segment: PipeSegment):
        self.segments.append(segment)

    def add_segments_from_dict(self, segments_dict: List[Dict]):
        """
        Метод для добавления сегментов из списка словарей
        Каждый словарь должен содержать параметры сегмента
        """
        for segment_params in segments_dict:
            try:
                # Создаем объект PipeSegment из словаря
                segment = PipeSegment(
                    dn_m=segment_params.get('dn_m', 100),
                    material=segment_params.get('material', 'steel'),
                    length_m=segment_params.get('length_m', 1),
                    thickness_m=segment_params.get('thickness_m', 0.025),
                    isolation_lambda=segment_params.get('isolation_lambda', 0.05),
                    tin=segment_params.get('tin', 65),
                    tout=segment_params.get('tout', 18)
                )
                self.segments.append(segment)
            except Exception as e:
                print(f"Ошибка при создании сегмента: {e}")

    def to_df(self) -> pd.DataFrame:
        data = [segment.to_dict() for segment in self.segments]
        return pd.DataFrame(data)

    def total_heat_loss(self) -> float:
        return sum(segment.Qloss_W for segment in self.segments)