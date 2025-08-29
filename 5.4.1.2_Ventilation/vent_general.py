# import pandas as pd
# from scipy.interpolate import interp1d



def calculate_airVelocity_m_s(
    flow_m3_h: float,  
    a_side_m: float = 0, 
    b_side_m: float = 0, 
    diameter_m: float = 0,
    square_m2: float = 0,
    shape: str = "rect",  
) -> float:
    """
    Calculation of air velocity in the duct.

    The function calculates the air flow velocity in meters per second based on
    the specified air flow rate and duct cross-section area.

    Parameters:
    flow_m3_h (float): Air flow rate in cubic meters per hour
    a_side_m (float): Length of the rectangular section side (m)
    b_side_m (float): Width of the rectangular section side (m)
    square_m2 (float): Duct cross-section area (m²)
    shape (str): Section shape ("rect" - rectangular, "circle" - circular)

    Return value:
    float: Air velocity in meters per second

    Notes:
    - For a rectangular section, you can specify either sides a and b,
      or the total area square_m2
    - For a circular section, it is necessary to specify the area square_m2
    - If the section shape is incorrect, returns 0
    """
    try:
        if shape not in ("rect", "circle"):
            raise ValueError("Invalid section shape. Valid values: 'rect' or 'circle'")

        if shape == "rect":
            # If area is not specified, calculate it through sides
            if square_m2 == 0:
                if a_side_m == 0 or b_side_m == 0:
                    raise ValueError("For a rectangular section, it is necessary to specify sides or area")
                square_m2 = a_side_m * b_side_m
        elif shape == "circle":
            if square_m2 == 0:
                square_m2 = round(3.1415 * ((diameter_m**2) / 4), 3)

        print(f"square_m2 = {square_m2}")

        # Air velocity calculation
        velosity_m_s = round(flow_m3_h / (3600 * square_m2), 3)
        
        return velosity_m_s

    except Exception as e:
        print(f"Error during calculation: {str(e)}")
        return 0.0
    

def calculate_air_heating_power_kW(
    flow_m3_h: float,  
    temp_in: float,    
    temp_out: float,   
    air_density: float = 1.2,  
    specific_heat: float = 1.005  
) -> float:
    """
    Calculates the required heating power to heat air from one temperature to another.

    The function computes the power required to heat a specified air flow from the inlet
    temperature to the desired outlet temperature.

    Parameters:
    flow_m3_h (float): Air flow rate in cubic meters per hour
    temp_in (float): Inlet air temperature in degrees Celsius
    temp_out (float): Desired outlet air temperature in degrees Celsius
    air_density (float): Air density in kg/m³ (default: 1.2)
    specific_heat (float): Specific heat capacity of air in kJ/kg·°C (default: 1.005)

    Returns:
    float: Required heating power in kilowatts (kW)

    Formula:
    Q = L × ρ × c × Δt / 3600
    where:
    Q - required heating power (kW)
    L - air flow rate (m³/h)
    ρ - air density (kg/m³)
    c - specific heat capacity of air (kJ/kg·°C)
    Δt - temperature difference (°C)
    """
    try:
        # Validate input parameters
        if flow_m3_h <= 0:
            raise ValueError("Air flow rate must be greater than zero")
        if air_density <= 0:
            raise ValueError("Air density must be greater than zero")
        if specific_heat <= 0:
            raise ValueError("Specific heat capacity must be greater than zero")

        # Calculate temperature difference
        temp_diff = temp_out - temp_in
        
        # Check if heating is required
        if temp_diff <= 0:
            raise ValueError("Outlet temperature must be higher than inlet temperature")

        # Calculate required heating power
        power_kw = round((flow_m3_h * air_density * specific_heat * temp_diff) / 3600, 3)
        
        return power_kw

    except Exception as e:
        print(f"Error during calculation: {str(e)}")
        return 0.0


def calculate_air_pressure_loss_Pa(
    flow_m3_h: float, 
    length_m: float, 
    a_side_m: float = 0, 
    b_side_m: float = 0, 
    diameter_m: float = 0, 
    shape: str = "rect", 
    air_density: float = 1.205, 
    kinematic_viscosity: float = 1.49619e-5,
    roughness: float = 0.0001 
) -> float:
    """
    Calculates pressure loss in a straight section of ductwork.

    The function computes pressure loss based on air flow, duct dimensions, and material properties.

    Parameters:
    flow_m3_h (float): Air flow rate in cubic meters per hour
    length_m (float): Length of the duct section (m)
    a_side_m (float): Length of the rectangular section side (m)
    b_side_m (float): Width of the rectangular section side (m)
    diameter_m (float): Diameter of circular duct (m)
    shape (str): Duct shape ("rect" - rectangular, "circle" - circular)
    air_density (float): Air density (kg/m³)
    kinematic_viscosity (float): Kinematic viscosity of air (m²/s)
    roughness (float): Internal surface roughness (m)

    Returns:
    float: Pressure loss in Pascals (Pa)
    """
    try:
        # Validate input parameters
        if flow_m3_h <= 0:
            raise ValueError("Flow rate must be positive")
        if length_m <= 0:
            raise ValueError("Duct length must be positive")
        
        # Calculate velocity
        velocity_m_s = calculate_airVelocity_m_s(
            flow_m3_h = flow_m3_h,
            a_side_m = a_side_m, 
            b_side_m = b_side_m, 
            diameter_m = diameter_m,
            shape = shape  
        )
        print(f"velocity_m_s = {velocity_m_s}")
        
        # Calculate equivalent diameter for rectangular ducts
        if shape == "rect":
            if a_side_m <= 0 or b_side_m <= 0:
                raise ValueError("Both sides of rectangular duct must be specified")
            equivalent_diameter = (2 * a_side_m * b_side_m) / (a_side_m + b_side_m)
            area_m2 = a_side_m * b_side_m
        elif shape == "circle":
            if diameter_m <= 0:
                raise ValueError("Diameter must be specified for circular duct")
            equivalent_diameter = diameter_m
            area_m2 = 3.141592 * (diameter_m / 2) ** 2
        else:
            raise ValueError("Invalid duct shape. Use 'rect' or 'circle'")
            
        print(f"equivalent_diameter = {equivalent_diameter}")

        reynolds_number = velocity_m_s * equivalent_diameter / kinematic_viscosity
        print(f"reynolds_number = {reynolds_number}")
        dynamic_pressure_pa = 0.5 * air_density * (velocity_m_s ** 2)
        print(f"dynamic_pressure_pa = {dynamic_pressure_pa}")

        if reynolds_number < 100 and reynolds_number > 0:
            # Calculate friction coefficient laminar flow
            friction_coefficient = 0.3164/((reynolds_number) ** 0.25)
        # elif reynolds_number > 1e5:
        elif reynolds_number > 100:
            # Calculate friction coefficient turbulent flow (А. Д. Альтшуль - МИСИ)
            friction_coefficient = 0.11 * ((roughness / equivalent_diameter) + (68 / reynolds_number)) ** 0.25
        else:
            raise ValueError(f"Error with reynolds_number = {reynolds_number}")
        
        print(f"friction_coefficient = {friction_coefficient}")

        # Calculate total pressure loss (Henry Philibert Gaspard Darcy - Julius Ludwig Weisbach)
        pressure_loss_pa = friction_coefficient * (length_m / equivalent_diameter) * dynamic_pressure_pa
        
        return int(pressure_loss_pa)

    except Exception as e:
        print(f"Error during calculation: {str(e)}")
        return 0.0
