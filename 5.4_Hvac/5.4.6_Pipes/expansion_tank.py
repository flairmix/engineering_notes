from enum import Enum


class Object():
    def __init__(self, id):
        self.id = id
        self.id_list = []


class System(Object):
    def __init__(self, id):
        self.id = id
        self.system_type = Enum()


class Equipment(Object):
    def __init__(self, id):
        self.id = id
        self.id_list.append(id)

class Expansion_tank(Equipment):    
    """
    return dp for Gmax consumption with kvs
    G - t/h 
    """
    def __init__(self, id, power_Gcal, temp_t1, temp_t2, static_pressure, valve_pressure):
            super().__init__(id)

            self.power_Gcal = power_Gcal 
            self.temp_t1 = temp_t1 
            self.temp_t2 = temp_t2 
            self.static_pressure = static_pressure 
            self.valve_pressure = valve_pressure
            self.active_agent = 'water'

            self.manufacturer = " "
            self.volume_unit = 15
    
            #expansion water
            agents = ['water']

            temp = [10, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95, 100, 105, 110, 115, 120, 130]
            expansion = [0.0003, 0.0017, 0.0043, 0.0078, 0.0121, 0.0171, 0.228, 0.0292, 0.0326, 0.0361, 0.0398, 0.0434, 0.0477, 0.519, 0.0562, 0.0606, 0.0606]

            i = 0 
            while(temp_t1 > temp[i]):
                i += 1
            self.coef_expansion = expansion[i]

            self.system_volume_l = self.power_Gcal * 1163 * self.volume_unit 
            self.expansion_volume = 1.05 * (self.system_volume_l * self.coef_expansion)
            self.tank_volume = int(self.expansion_volume / (1 - (self.static_pressure / self.valve_pressure)))

    def change_agent(agent:str):
        pass
        
    def tank_volume_manually(self, system_volume_l):
        expansion_volume = 1.05 * (system_volume_l * self.coef_expansion)
        return int(expansion_volume / (1 - (self.static_pressure / self.valve_pressure)))
    
    def report_print(self):
        print(f"Бак расширительный - {self.id}\n\
                Нагрузка системы, Гкал/ч - {self.power_Gcal}\n\
                Температурный график t1/t2 - {self.temp_t1} / {self.temp_t2}\n\
                Давление статическое системы, бар - {self.static_pressure}\n\
                Давление сраб.предохранительного клапана, бар - {self.valve_pressure}\n\
                Объем системы удельный, л/кВт - {self.volume_unit}\n\
                Коэфициент расширения, - {self.coef_expansion}\n\
                Объем расширения, м3 - {self.expansion_volume}\n\
                Объем расширительного бака расчетный, м3 - {self.tank_volume}\n\
                ")
    
