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

default_write_path = "out/"


class OSOMVariables(str, Enum):
    SALINITY_BOTTOM = "SalinityBottom"
    SALINITY_SURFACE = "SalinitySurface"
    WATER_TEMPERATURE_BOTTOM = "WaterTempBottom"
    WATER_TEMPERATURE_SURFACE = "WaterTempSurface"
    SURFACE_HEIGHT = "SurfaceHeight"
    VELOCITY_EASTWARD_BOTTOM = "VelocityEastwardBottom"
    VELOCITY_EASTWARD_SURFACE = "VelocityEastwardSurface"
    VELOCITY_NORTHWARD_BOTTOM = "VelocityNorthwardBottom"
    VELOCITY_NORTHWARD_SURFACE = "VelocityNorthwardSurface"
    KINETIC_ENERGY_BOTTOM = "KineticEnergyBottom"
    KINETIC_ENERGY_SURFACE = "KineticEnergySurface"


ALL_VARIABLES = [
    OSOMVariables.SALINITY_BOTTOM,
    OSOMVariables.SALINITY_SURFACE,
    OSOMVariables.WATER_TEMPERATURE_BOTTOM,
    OSOMVariables.WATER_TEMPERATURE_SURFACE,
    OSOMVariables.SURFACE_HEIGHT,
    OSOMVariables.VELOCITY_EASTWARD_BOTTOM,
    OSOMVariables.VELOCITY_EASTWARD_SURFACE,
    OSOMVariables.VELOCITY_NORTHWARD_BOTTOM,
    OSOMVariables.VELOCITY_NORTHWARD_SURFACE,
    OSOMVariables.KINETIC_ENERGY_BOTTOM,
    OSOMVariables.KINETIC_ENERGY_SURFACE,
]
