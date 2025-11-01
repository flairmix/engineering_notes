import math

# Константы для конвертации
GCAL_TO_KW = 1163.0
KW_TO_GCAL = 1/1163.0
PI = math.pi

# Доступные стандартные диаметры труб в мм
STANDARD_DN = [20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200, 250, 300]

def gcalh_to_kw(power_gcalh: float) -> float:
    """
    Конвертация Гкал/ч в кВт
    :param power_gcalh: мощность в Гкал/ч
    :return: мощность в кВт
    """
    return round(power_gcalh * GCAL_TO_KW, 3)

def kw_to_gcalh(power_kw: float) -> float:
    """
    Конвертация кВт в Гкал/ч
    :param power_kw: мощность в кВт
    :return: мощность в Гкал/ч
    """
    return round(power_kw * KW_TO_GCAL, 3)

def calculate_flow_rate(
    power_gcalh: float,
    temp_high: float = 130.0,
    temp_low: float = 70.0
) -> float:
    """
    Расчет расхода теплоносителя
    :param power_gcalh: мощность в Гкал/ч
    :param temp_high: температура подачи (°C)
    :param temp_low: температура обратки (°C)
    :return: расход в т/ч
    """
    if temp_high <= temp_low:
        raise ValueError("Температура подачи должна быть выше температуры обратки")
    return round(1000 * power_gcalh / (temp_high - temp_low), 2)

def select_pipe_diameter(
    flow_rate: float,
    velocity: float = 1.0
) -> int:
    """
    Подбор диаметра трубы по расходу
    :param flow_rate: расход в т/ч
    :param velocity: скорость потока (м/с)
    :return: диаметр трубы (мм)
    """
    if flow_rate <= 0:
        raise ValueError("Расход должен быть положительным")
    
    calculated_dn = 1000 * math.sqrt(flow_rate / (2826 * velocity))
    
    for dn in STANDARD_DN:
        if calculated_dn <= dn:
            return dn
    raise ValueError("Не удалось подобрать диаметр трубы")

def calculate_velocity(
    flow_rate: float,
    diameter: float
) -> float:
    """
    Расчет скорости потока
    :param flow_rate: расход в т/ч
    :param diameter: диаметр трубы (мм)
    :return: скорость потока (м/с)
    """
    if diameter <= 0:
        raise ValueError("Диаметр трубы должен быть положительным")
    return round(1e6 * flow_rate / (diameter**2 * 2826), 2)

def calculate_kv(
    max_flow: float,
    min_pressure_drop: float
) -> float:
    """
    Расчет коэффициента пропускной способности
    :param max_flow: максимальный расход (м³/ч)
    :param min_pressure_drop: минимальный перепад давления (бар)
    :return: коэффициент kv
    """
    if min_pressure_drop <= 0:
        raise ValueError("Перепад давления должен быть положительным")
    return max_flow / math.sqrt(min_pressure_drop)

def calculate_flow_by_dn_and_v_t_per_h(
    diameter: float,
    velocity: float
) -> float:
    """
    Расчет расхода по диаметру трубы и скорости потока в т/ч
    :param diameter: диаметр трубы (мм)
    :param velocity: скорость потока (м/с)
    :return: расход (т/ч)
    """
    if diameter <= 0:
        raise ValueError("Диаметр трубы должен быть положительным")
    if velocity <= 0:
        raise ValueError("Скорость потока должна быть положительной")
    
    # Формула: Q = v * A * 3600, где A - площадь сечения трубы
    area = PI * (diameter / 2000) ** 2  # Площадь сечения в м²
    flow = velocity * area * 3600  # Расход в м³/ч
    return round(flow, 2)  # Преобразование в т/ч (плотность воды ~1000 кг/м³)


def optimize_diameters(required_flow: float, v_min=0.6, v_max=1.0) -> int:
    """
    Оптимизированный подбор диаметра с сохранением DN25 и DN32
    :param required_flow: требуемый расход (т/ч)
    :return: оптимальный диаметр трубы (DN)
    """
    optimized_dn = []
    for dn in STANDARD_DN:
        optimized_dn.append((dn, calculate_flow_by_dn_and_v_t_per_h(dn, v_min), calculate_flow_by_dn_and_v_t_per_h(dn, v_max)))

    if required_flow < 2.0:
        return 25
    elif required_flow > 254.47:
        raise ValueError("Требуется диаметр больше DN300")
    
    for dn, min_flow, max_flow in optimized_dn:
        if min_flow <= required_flow <= max_flow:
            return dn
    
    # Корректировка для пограничных значений
    for dn, min_flow, max_flow in optimized_dn:
        if required_flow <= max_flow:
            return dn
