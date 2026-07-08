"""
A module containing constants used in the application.
"""

from enum import Enum

LON_W = -72.7
LON_E = -69.96
LAT_N = 41.9
LAT_S = 40.5

default_height = 160 * 20
default_width = 260 * 20


class OSOMVariables(str, Enum):
    TEMP = "WaterTemp"
    SALT = "Salinity"
    VELOCITY_E = "VelocityEastward"
    VELOCITY_N = "VelocityNorthward"
    KINETIC_ENERGY = "KineticEnergy"


class SurfaceOrBottom(str, Enum):
    SURFACE = "Surface"
    BOTTOM = "Bottom"


"""

variables(dimensions):

float32 SalinityBottom(ocean_time, eta_rho, xi_rho),
float32 SalinitySurface(ocean_time, eta_rho, xi_rho),
float32 WaterTempBottom(ocean_time, eta_rho, xi_rho),
float32 WaterTempSurface(ocean_time, eta_rho, xi_rho),
float32 SurfaceHeight(ocean_time, eta_rho, xi_rho),
float32 VelocityEastwardBottom(ocean_time, eta_rho, xi_rho),
float32 VelocityEastwardSurface(ocean_time, eta_rho, xi_rho),
float32 VelocityNorthwardBottom(ocean_time, eta_rho, xi_rho),
float32 VelocityNorthwardSurface(ocean_time, eta_rho, xi_rho),
float32 KineticEnergyBottom(ocean_time, eta_rho, xi_rho),
float32 KineticEnergySurface(ocean_time, eta_rho, xi_rho),

float64 ocean_time(ocean_time)



00. 00:00
01. 01:30
02. 03:00
03. 04:30
04. 06:00
05. 07:30
06. 09:00
07. 10:30
08. 12:00
09. 13:30
10. 15:00
11. 16:30
12. 18:00
13. 19:30
14. 21:00
15. 22:30

16. 24:00

"""
