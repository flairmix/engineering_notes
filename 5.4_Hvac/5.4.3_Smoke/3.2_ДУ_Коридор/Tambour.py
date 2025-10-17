from typing import Literal

class Tambour:
    '''

    types:
        '4.3.1' - 
        '4.3.2' - 
        '4.3.3' - 
    '''
    def __init__(self,
                 type: Literal['4.3.1', '4.3.2', '4.3.3'] = '4.3.1',
                 location_type: Literal['above-ground', 'underground'] = 'above-ground',
                 door_square_m2: float = 3.0,
                 air_velocity_regulated_m_s: float = 1.3,
                 density_air: float = (353/(273-26)),
                 number_of_doors: int = 1,
                 ):
        self.type = type
        self.location_type = location_type
        self.door_square_m2 = door_square_m2
        self.air_velocity_regulated_m_s = air_velocity_regulated_m_s
        self.density_air = density_air
        self.number_of_doors = number_of_doors
        if type == '4.3.1':
            self.flow_pressurization_kg_s = self.calc_pressurization_kg_s_431(self.door_square_m2, self.air_velocity_regulated_m_s, self.density_air)
        elif type == '4.3.2':
            self.flow_pressurization_kg_s = self.calc_pressurization_kg_s_432(self.door_square_m2, density_air, self.number_of_doors)
        elif type == '4.3.3':
            pass
        else:
            self.flow_pressurization_kg_s = None
            print('Неверный тип тамбура')

        self.flow_pressurization_m3_h = round(self.flow_pressurization_kg_s * 3600 / self.density_air, 3)

    def calc_pressurization_kg_s_431(self, 
                                    door_square_m2, 
                                    air_velocity_regulated_m_s, 
                                    density_a,
                                    ) -> float:
        '''
        4.3.1. Расход воздуха, подаваемого в тамбур-шлюзы, расположенные 
        - при выходах в незадымляемые лестничные клетки типа НЗ;
        - или Н2 (в высотных многофункциональных зданиях и комплексах, в жилых зданиях высотой более 75 м, в общественных зданиях высотой более 50 м);
        - во внутренние открытые лестницы 2-го типа;
        - на входах в атриумы и пассажи с уровней подвальных и цокольных этажей;
        - перед лифтовыми холлами подземных автостоянок;
        - а также в тамбур-шлюзы при выходах в вестибюли из незадымляемых лестничных клеток типа Н2, сообщающихся с надземными этажами зданий различного назначения;
        - имеющих режим управления "перевозка пожарных подразделений" в цокольных, подвальных, подземных этажах;

        SP60_9.11 
        Для тамбур-шлюза, расположенного на пути эвакуации и предназначенного для входа в него из двух и более раздельных помещений, 
        подачу воздуха системой приточной противодымной вентиляции следует определять из расчета необходимости обеспечения скорости истечения воздуха, 
        равной 1,3 м/с, только через один дверной проем наибольшей площади.

        Gr = air_velocity_regulated_m_s * door_squre_m2 * density_a, (59)

        air_velocity_regulated_m_s > 1,3 м/с.
        '''
        return round(air_velocity_regulated_m_s * density_a * door_square_m2, 3)


    def calc_pressurization_kg_s_432(self, 
                                    door_square_m2, 
                                    density_a = 353/(273-26),
                                    number_of_doors = 1,
                                    Sdr = None
                                    ) -> float:
        '''
        4.3.2. Расход воздуха, подаваемого в тамбур-шлюзы
        - отделяющие помещения для хранения автомобилей закрытых надземных и подземных автостоянок от помещений иного назначения,
        - отделяющие помещения для хранения автомобилей от изолированных рамп подземных автостоянок
        '''
        if Sdr is None:
            Sdr = 5300 / density_a

        return round(number_of_doors*door_square_m2*((20/Sdr)**0.5), 3)
    

    def calc_pressurization_kg_s_433(self,
                                     n = 1,
                                     F_dr = 1.0*2.2,
                                     m = 0,
                                     F_dl = 0.7*2.2,
                                     density_a = 1.21,
                                      ) -> float:
        """
        4.3.3. Расход воздуха, подаваемого в тамбур-шлюзы (лифтовые холлы)
        - при выходах из лифтов с режимом управления "пожарная опасность" в цокольные, подвальные, подземные этажи зданий различного назначения;
            
        Рассчитывает значение G_r по формуле:
        G_r = n * F_dr * (20 / S_dr)^(1/2) + m * F_dl * (20 / S_dl)^(1/2)
        
        Параметры:
        n (int): количество дверей защищаемого тамбур-шлюза
        F_dr (float): характеристика удельного сопротивления воздухопроницанию дверей защищаемого тамбур-шлюза
        S_dr (float): характеристика удельного сопротивления воздухопроницанию дверей защищаемого тамбур-шлюза
        m (int): количество дверей лифтовой шахты
        F_dl (float): характеристика удельного сопротивления воздухопроницанию дверей лифтовой шахты
        S_dl (float): характеристика удельного сопротивления воздухопроницанию дверей лифтовой шахты
        
        Возвращает:
        float: значение G_r
        """
        S_dr = 5300 / density_a
        S_dl = 2600 / density_a

        term1 = n * F_dr * (20 / S_dr) ** 0.5
        term2 = m * F_dl * (20 / S_dl) ** 0.5
        
        return round(term1 + term2, 3)


    def calculate_pressure_above_ground(h_i, h_dri, rho_a, rho_r, g=9.81):
        """
        Рассчитывает давление в надземной части тамбур-шлюзов.
        
        Параметры:
        h_i (float): высота тамбур-шлюза на i-м этаже, м
        h_dri (float): высота дверных проемов тамбур-шлюзов на i-м этаже, м
        rho_a (float): плотность наружного воздуха, кг/м³
        rho_r (float): плотность воздуха в помещении, кг/м³
        g (float): ускорение свободного падения, м/с²
        
        Возвращает:
        float: давление в Па
        """
        return int(20 - g * (h_i + 0.5 * h_dri) * (rho_a - rho_r))

    def calculate_pressure_below_ground(h_n, h_i, h_dri, rho_a, rho_r, g=9.81):
        """
        Рассчитывает давление в подземной части тамбур-шлюзов.
        
        Параметры:
        h_n (float): глубина подземной части, м
        h_i (float): высота тамбур-шлюза на минус i-м этаже, м
        h_dri (float): высота дверных проемов тамбур-шлюзов на минус i-м этаже, м
        rho_a (float): плотность наружного воздуха, кг/м³
        rho_r (float): плотность воздуха в помещении, кг/м³
        g (float): ускорение свободного падения, м/с²
        
        Возвращает:
        float: давление в Па
        """
        return int(20 + g * (h_n - (h_i + 0.5 * h_dri)) * (rho_a - rho_r))