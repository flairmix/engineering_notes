import math
from typing import Literal

def calculate_infiltration_Pamfilova(
    temp_in: float = 18,
    temp_out: float = -23,
    building_height_m: float = 75,
    winf_velocity_m_s: float = 1.7,
    localization: Literal['ru', 'en'] = 'ru',
) -> float:
    """
    Рассчитывает коэффициент инфильтрации по методу Памфилова.

    Метод учитывает влияние гравитационного и ветрового давления на воздухопроницаемость здания.
    Формула объединяет эффект естественной тяги (из‑за разницы температур) и ветрового напора.

    Формула:
    K = 0.01 × √[2 × g × H × (1 − (T_нар / T_внутр)) + V²]
    где:
        g = 9.81 м/с² — ускорение свободного падения;
        H — высота здания (м);
        T_нар = 273 + t_нар — абсолютная температура наружного воздуха (К);
        T_внутр = 273 + t_внутр — абсолютная температура внутреннего воздуха (К);
        V — скорость ветра (м/с).

    Параметры:
        temp_in (float): Температура внутри помещения (°C). По умолчанию 20 °C.
        temp_out (float): Температура наружного воздуха (°C). По умолчанию −26 °C.
        building_height_m (float): Высота здания (м). По умолчанию 75 м.
        winf_velocity_m_s (float): Скорость ветра (м/с). По умолчанию 1 м/с.

    Возвращает:
        float: Коэффициент инфильтрации K (безразмерная величина).

    Исключения:
        TypeError: Если типы аргументов не соответствуют ожидаемым (float/int).
        ValueError: 
            - Если building_height_m ≤ 0 (некорректная высота здания).
            - Если winf_velocity_m_s < 0 (отрицательная скорость ветра).
            - Если расчёт приводит к извлечению квадратного корня из отрицательного числа.
    """
    try:
        # Проверка типов аргументов
        if not isinstance(temp_in, (int, float)):
            raise TypeError("temp_in должен быть числом (int или float)")
        if not isinstance(temp_out, (int, float)):
            raise TypeError("temp_out должен быть числом (int или float)")
        if not isinstance(building_height_m, (int, float)):
            raise TypeError("building_height_m должен быть числом (int или float)")
        if not isinstance(winf_velocity_m_s, (int, float)):
            raise TypeError("winf_velocity_m_s должен быть числом (int или float)")

        # Валидация значений
        if building_height_m <= 0:
            raise ValueError("building_height_m должно быть положительным числом")
        if winf_velocity_m_s < 0:
            raise ValueError("winf_velocity_m_s не может быть отрицательным")

        # Перевод температур в абсолютные (Кельвины)
        temp_in_k = 273 + temp_in
        temp_out_k = 273 + temp_out

        # Проверка на корректность отношения температур (чтобы подкоренное выражение было ≥ 0)
        if temp_out_k / temp_in_k >= 1:
            raise ValueError(
                "Отношение наружных к внутренним температурам в Кельвинах ≥ 1. "
                "Это приведёт к отрицательному подкоренному выражению"
            )

        # Основной расчёт
        g = 9.81  # ускорение свободного падения, м/с²
        inner_sqrt = 2 * g * building_height_m * (1 - (temp_out_k / temp_in_k)) + winf_velocity_m_s ** 2

        if inner_sqrt < 0:
            raise ValueError(f"Подкоренное выражение отрицательно: {inner_sqrt:.4f}")

        result = 0.01 * math.sqrt(inner_sqrt)
        label_ru = "Коэффициент инфильтрации K"
        label_en = "Coefficient infiltration K"

        if localization == 'en':
            label = label_en
        else: 
            label = label_ru

        return {
            label : round(result, 3),
            }

    except TypeError as e:
        print(f"Ошибка типа данных: {e}")
        raise
    except ValueError as e:
        print(f"Некорректное значение параметра: {e}")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise
