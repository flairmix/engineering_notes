

def calculate_air_density_by_temp_kg_m3(
    absolute_temperature_K: float = 273 + 20,  # Absolute temperature in Kelvin (default is 293 K, corresponding to 20°C)
    absolute_pressure_Pa: float = 101325,      # Absolute pressure in Pascals (default is 101,325 Pa, standard atmospheric pressure)
    gas_constant: float = 8.31446261815324,  # Universal gas constant, J/(mol·K)
    molar_mass_of_dry_air: float = 0.0289652   # Molar mass of dry air, kg/mol
) -> float:
    """
    Calculates the density of dry air (in kg/m³) based on the given temperature and pressure,
    using the ideal gas equation (the Mendeleev-Clapeyron equation):
    ρ = P * M / (R * T), where:
    - ρ is the density of the gas, kg/m³;
    - P is the pressure, Pa;s
    - M is the molar mass of the gas, kg/mol;
    - R is the universal gas constant, J/(mol·K);
    - T is the absolute temperature, K.

    Parameters:
        absolute_temperature_K (float): Absolute temperature of air in Kelvin.
        absolute_pressure_Pa (float): Absolute pressure of air in Pascals.
        gas_constant (float): Universal gas constant (default is 8.31446261815324 J/(mol·K)).
        molar_mass_of_dry_air (float): Molar mass of dry air (default is 0.0289652 kg/mol).

    Returns:
        float: Air density in kilograms per cubic meter (kg/m³), rounded to 4 decimal places.

    Example usage:
        >>> density = calculate_density_by_temp_kg_m3(293, 101325)
        >>> print(density)
        1.2048
    """
    density = absolute_pressure_Pa * molar_mass_of_dry_air / (gas_constant * absolute_temperature_K)
    return round(density, 4)


def delta_pressure(t_inside, t_outside, height):
    """
    Рассчитывает разницу давлений (Па) из-за естественной тяги
    по температурам внутри/снаружи и высоте над уровнем земли.

    Параметры:
        t_inside (float): температура внутри, °C
        t_outside (float): температура снаружи, °C
        height (float): высота точки расчёта над уровнем земли, м

    Возвращает:
        float: разница давлений ΔP (Па).
            > 0: внутреннее давление выше (воздух выходит)
            < 0: наружное давление выше (воздух входит)
    """
    # Физические константы
    g = 9.81  # м/с²
    p0 = 101325  # Па (стандартное атмосферное давление)
    M = 0.02896  # кг/моль (молярная масса воздуха)
    R = 8.314  # Дж/(моль·К)

    # Перевод температур в Кельвины
    T_inside = t_inside + 273.15
    T_outside = t_outside + 273.15

    # Плотность воздуха: ρ = p0 * M / (R * T)
    rho_inside = p0 * M / (R * T_inside)
    rho_outside = p0 * M / (R * T_outside)

    # Разница давлений: ΔP = g * H * (ρ_нар − ρ_внутр)
    delta_p = round(g * height * (rho_outside - rho_inside), 4)

    return delta_p
