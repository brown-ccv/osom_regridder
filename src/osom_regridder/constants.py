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
    TEMP = "temp"
    SALT = "salt"
    ZETA = "zeta"
    UBAR_EAST = "ubar_eastward"
    UBAR_WEST = "ubar_westward"
    KINETIC_ENERGY = "AKv"


class SurfaceOrBottom(str, Enum):
    SURFACE = "surface"
    BOTTOM = "bottom"
