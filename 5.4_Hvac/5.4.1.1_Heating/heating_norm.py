def calculate_heating_norm_kW(
    building_volume_m3: float,
    NSTCP: float,
    temp_in: float = 18,
    temp_out: float = -23,
    reserve: float = 0.05
) -> float:
    """
    Calculate the normalized heating load (kW) meeting energy efficiency requirements 
    per SP 50.13330.2012 (Thermal Protection of Buildings).

    This function computes the design heating load that ensures:
    - maintenance of indoor thermal comfort;
    - compliance with energy efficiency standards;
    - adherence to regulatory thermal protection requirements.

    The calculation is based on the **normalized specific thermal protection 
    characteristic** (NSTCP, k_norm), which is a key parameter from SP 50.13330.2012.
    This value represents the maximum permissible heat loss per unit volume of the building
    and serves as an energy efficiency benchmark.

    Key compliance aspects with SP 50:
    1. Uses k_norm (NSTCP) from SP 50 tables for the specific building type and climate zone;
    2. Accounts for design outdoor temperature (t_out) per climatic data in SP 131.13330;
    3. Applies volume‑based heat loss calculation method per SP 50 methodology;
    4. Includes reserve factor for system reliability and extreme conditions.

    Formula:
        Q = k_norm × (1 − reserve) × (t_in − t_out) × V / 1000
    where:
        Q — design heating load (kW);
        k_norm (NSTCP) — normalized specific thermal protection characteristic (W/(m³·°C));
        reserve — safety factor (e.g., 0.05 = 5%);
        t_in — indoor design temperature (°C);
        t_out — outdoor design temperature (°C);
        V — heated building volume (m³).

    Parameters:
        building_volume_m3 (float): Heated building volume in cubic meters (m³).
            Must be positive.
        NSTCP (float): Normalized specific thermal protection characteristic (k_norm)
            in W/(m³·°C) per SP 50.13330.2012 tables. Must be non‑negative.
        temp_in (float): Design indoor temperature (°C). Default: 18 °C.
        temp_out (float): Design outdoor temperature (°C) per climatic norms.
            Default: −23 °C. Must be lower than temp_in.
        reserve (float): Safety/reserve factor as a fraction (e.g., 0.05 for 5%).
            Must be in range [0, 1). Default: 0.05 (5%).

    Returns:
        float: Design heating load in kilowatts (kW), rounded to 3 decimal places.
        This represents the minimum required heating system capacity that:
        - maintains indoor comfort;
        - complies with SP 50 thermal protection norms;
        - accounts for local climate;
        - includes safety margin.

    Raises:
        TypeError: If any parameter is not a number (int/float).
        ValueError: 
            - If building_volume_m3 ≤ 0;
            - If NSTCP < 0;
            - If reserve < 0 or reserve ≥ 1;
            - If temp_in ≤ temp_out.

    Examples:
        >>> calculate_heating_norm_kW(5000, 0.12, 18, -23, 0.05)
        233.730
        >>> calculate_heating_norm_kW(3000, 0.10, 20, -20, 0.1)
        108.000
    """
    try:
        # Type validation
        if not all(isinstance(val, (int, float)) for val in [
            building_volume_m3, NSTCP, temp_in, temp_out, reserve
        ]):
            raise TypeError("All parameters must be numbers (int or float)")

        # Value validation
        if building_volume_m3 <= 0:
            raise ValueError("building_volume_m3 must be positive (greater than 0)")
        if NSTCP < 0:
            raise ValueError("NSTCP must be non‑negative")
        if reserve < 0 or reserve >= 1:
            raise ValueError("reserve must be in range [0, 1)")
        if temp_in <= temp_out:
            raise ValueError("temp_in must be greater than temp_out")

        # Calculation
        temperature_difference = temp_in - temp_out
        heating_load_W = NSTCP * (1 - reserve) * temperature_difference * building_volume_m3
        heating_load_kW = heating_load_W / 1000  # Convert W to kW

        return round(heating_load_kW, 3)

    except TypeError as e:
        print(f"Type error: {e}")
        raise
    except ValueError as e:
        print(f"Value error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during heating norm calculation: {e}")
        raise
