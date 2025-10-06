**Calculation of Heat Flow for Radiators**

The formula for calculating the heat flow of a radiator under conditions different from normal (95/85/20°C, coolant flow rate 0.1 kg/s) is as follows:

$Q = Q_{\text{nom}} \cdot \left(\frac{\theta}{70}\right)^n \cdot b \cdot k \cdot p$

Where:
- $Q_{\text{nom}}$ is the nominal heat flow of the radiator under normal conditions [W].
- $\theta$ is the actual temperature difference [°C].
- $t_h$ and $t_k$ are the initial and final temperatures of the coolant (at the inlet and outlet) in the heating device [°C].
- $t_p$ is the calculated room temperature, equal to the calculated air temperature in the heated room [°C].
- $n$ is an empirical exponent for the relative temperature difference.
- $b$ is a dimensionless correction factor for the calculated atmospheric pressure.
- $k$ is the coefficient for single-sided connection.

**Example Calculation:**

For a coolant flow rate of 0.015–0.15 kg/s (54–540 kg/h), the coefficients are $c = 1$, $m = 0$, $p = 1$. The formula simplifies to:

$Q = Q_{\text{nom}} \cdot \left(\frac{\theta}{70}\right)^n \cdot b \cdot k$

**Movement of Coolant:**
- For "top-down" movement, the coefficients are as follows:
  - $n = 0.26$ for 10–300, 10–500, and 11–500.
  - $n = 0.3$ for 20–300 and 20–500.
  - $n = 0.28$ for 20–200, 202–300, and 202–500.
  - $n = 0.3$ for 21–300, 21–500, 22–300, and 22–500.
  - $n = 0.3$ for 30–500, 302–500, 33–300, and 33–500.

If you need further assistance or clarification, feel free to ask!