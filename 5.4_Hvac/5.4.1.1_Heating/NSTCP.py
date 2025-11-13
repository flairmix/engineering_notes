def calculation_NSTCP_W_m3C(
    GSOP: float,
    building_volume_m3: float,
) -> float:
    """
    Calculate Normalized Specific Thermal Protection Characteristic (NSTCP).
    (SP 50.13330.2012 (Thermal Protection of Buildings) 5.5)
    
    Computes the normalized specific thermal protection characteristic of a building 
    according to regulatory methodology. The result is the maximum of two calculated
    coefficients (k1 and k2) that account for climate conditions and building volume.

    Formula components:
      k1 = 8.5 / √GSOP
      k2 depends on building volume:
        - if volume ≤ 960 m³: 
          k2 = (4.74 / (0.00013×GSOP + 0.61)) × (1 / volume⁽¹/³⁾)
        - if volume > 960 m³:
          k2 = (0.16 + (10 / √volume)) / (0.00013×GSOP + 0.61)

    Parameters:
        GSOP (float): Degree-days of the heating period (ГСОП), unit: °C·days.
            Must be positive.
        building_volume_m3 (float): Building volume in cubic meters (m³).
            Must be positive.

    Returns:
        float: NSTCP value (W/(m³·°C)), rounded to 3 decimal places.

    Raises:
        TypeError: If input parameters are not numeric (int/float).
        ValueError: 
            - If GSOP ≤ 0 (invalid climate parameter).
            - If building_volume_m3 ≤ 0 (invalid building parameter).

    Examples:
        >>> calculation_NSTCP(4000, 800)
        0.135

    Notes:
        The function returns the maximum value between k1 and k2 as per regulatory 
        calculation methodology.
    """
    try:
        # Type validation
        if not isinstance(GSOP, (int, float)):
            raise TypeError("GSOP must be a number (int or float)")
        if not isinstance(building_volume_m3, (int, float)):
            raise TypeError("building_volume_m3 must be a number (int or float)")

        # Value validation
        if GSOP <= 0:
            raise ValueError("GSOP must be positive (greater than 0)")
        if building_volume_m3 <= 0:
            raise ValueError("building_volume_m3 must be positive (greater than 0)")

        # Calculation of k1
        k1 = 8.5 / (GSOP ** 0.5)

        # Calculation of k2 (depends on building volume)
        denominator = 0.00013 * GSOP + 0.61

        if building_volume_m3 <= 960:
            k2 = (4.74 / denominator) * (1 / (building_volume_m3 ** 0.333))
        else:
            k2 = (0.16 + (10 / (building_volume_m3 ** 0.5))) / denominator

        # Return maximum of k1 and k2, rounded to 3 decimals
        result = max(k1, k2)
        return round(result, 3)

    except TypeError as e:
        print(f"Type error: {e}")
        raise
    except ValueError as e:
        print(f"Value error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during NSTCP calculation: {e}")
        raise
