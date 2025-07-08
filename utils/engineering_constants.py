"""
Engineering constants and unit conversions
"""

# Physical constants
GRAVITY_MS2 = 9.81  # Acceleration due to gravity (m/s²)
ATMOSPHERIC_PRESSURE_PA = 101325  # Standard atmospheric pressure (Pa)

# Unit conversions
MM_TO_M = 1e-3
M_TO_MM = 1e3
KG_TO_N = GRAVITY_MS2
N_TO_KG = 1.0 / GRAVITY_MS2

# Material densities (kg/m³)
STEEL_DENSITY_KG_M3 = 7850
CONCRETE_DENSITY_KG_M3 = 2400
ALUMINUM_DENSITY_KG_M3 = 2700

# Common load factors
DEAD_LOAD_FACTOR = 1.2
LIVE_LOAD_FACTOR = 1.6
WIND_LOAD_FACTOR = 1.0
SEISMIC_LOAD_FACTOR = 1.0

# Safety factors
STRUCTURAL_SAFETY_FACTOR = 2.5
FOUNDATION_SAFETY_FACTOR = 3.0
FATIGUE_SAFETY_FACTOR = 2.0
