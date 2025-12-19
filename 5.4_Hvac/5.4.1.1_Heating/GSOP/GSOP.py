def calculate_GSOP(
    temp_in: float = 20,
    temp_out_heating_mid: float = -1.7,
    heating_duration_days: int = 202,
) -> int:
    """
    Рассчитывает градусо-сутки отопительного периода (ГСОП).

    ГСОП — показатель, характеризующий потребность в отоплении за отопительный период.
    Вычисляется как произведение разности температур внутри и снаружи на длительность
    отопительного периода в днях.

    Формула: ГСОП = (t_внутр − t_внеш) × продолжительность_отопительного_периода

    Параметры:
        temp_in (float): Температура внутри помещения (в °C). По умолчанию 20 °C.
        temp_out_heating_mid (float): Средняя температура наружного воздуха 
            за отопительный период (в °C). По умолчанию −1.7 °C (Москва).
        heating_duration_days (int): Продолжительность отопительного периода (в днях).
            По умолчанию 202 дня.

    Возвращает:
        int: Градусо-сутки отопительного периода (целое число).

    """
    try:
        # Проверка типов аргументов
        if not isinstance(temp_in, (int, float)):
            raise TypeError("temp_in должен быть числом (int или float)")
        if not isinstance(temp_out_heating_mid, (int, float)):
            raise TypeError("temp_out_heating_mid должен быть числом (int или float)")
        if not isinstance(heating_duration_days, int):
            raise TypeError("heating_duration_days должен быть целым числом (int)")

        # Проверка корректности значения длительности отопительного периода
        if heating_duration_days <= 0:
            raise ValueError("heating_duration_days должно быть положительным числом")

        # Расчет ГСОП
        gsop = (temp_in - temp_out_heating_mid) * heating_duration_days

        return int(gsop)

    except TypeError as e:
        print(f"Ошибка типа данных: {e}")
        raise
    except ValueError as e:
        print(f"Некорректное значение параметра: {e}")
        raise
    except OverflowError as e:
        print(f"Переполнение при вычислении: {e}")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise
