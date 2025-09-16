

def calculate_heat_flow(
    Q_nom_w: float, 
    t_1: float, 
    t_2: float, 
    t_p: float = 20, 
    n: float = 0.28,
    b: float = 1.0, 
    k: float = 0.95, 
    p: float = 1.0
) -> int:
    """
    Calculates the actual heat flow of a radiator under specified conditions.

    This function computes the heat output of a radiator based on the nominal heat flow
    and various correction factors for different operating conditions.

    Parameters:
    Q_nom_w (float): Nominal heat flow at standard conditions (95/70/20°C) in watts
    t_1 (float): Supply temperature of the water in degrees Celsius
    t_2 (float): Return temperature of the water in degrees Celsius
    t_p (float): Design room temperature in degrees Celsius
    n (float): Empirical exponent for temperature difference calculation
    b (float): Correction factor for atmospheric pressure
    k (float): Connection coefficient
    p (float): Flow rate correction factor (default: 1.0)

    Returns:
    int: Actual heat flow in watts

    Formula:
    Q = Q_nom_w * (theta/70)**(1+n) * b * k * p
    where theta = ((t_1 - t_2) / 2) - t_p
    """
    try:
        # Calculate temperature difference
        theta = ((t_1 + t_2) / 2) - t_p
        
        # Validate temperature difference
        if theta <= 0:
            raise ValueError("Temperature difference must be positive")
        
        # Calculate heat flow
        heat_flow = Q_nom_w * ((theta / 70) ** (1 + n)) * b * k * p
        
        return int(heat_flow
)
    except Exception as e:
        print(f"Error during calculation: {str(e)}")
        return 0.0

# Example usage:
# Q = calculate_heat_flow(
#     Q_nom_w=1000,    # Nominal heat flow (W)
#     t_1=95,        # Supply temperature (°C)
#     t_k=70,        # Return temperature (°C)
#     t_p=20,        # Room temperature (°C)
#     n=0.3,         # Empirical exponent
#     b=1.0,         # Atmospheric pressure correction
#     k=0.95         # Connection coefficient
# )
