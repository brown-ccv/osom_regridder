"""
This module contains utility functions to create map files between raw OSOM
dataset and regridded latitude / longitude datasets. Given the OSOM grid file
and output x / y dimensions, this will generate a map to determine RAW OSOM
points map to which output latitude / longitude cells.

Functions:
  determine_bounds: Determines grid bounds from the given OSOM dataset.
"""

import math
import numpy as np
from typing import Tuple

from .file_input import import_grid


def determine_bounds(
    coordinate_grid: np.ndarray, cell_count: int
) -> Tuple[float, float, float, float]:
    """
    Utility function to determine the bounds of the OSOM grid (either latitude or longitude).

    Parameters:
      coordinate_grid (np.ndarray): The coordinate grid provided by the OSOM
        grid file. Either latitude or longitude grid.
      cell_count (int): The number of output cells in this dimension.

    Returns:
      Tuple[float, float, float, float]: A tuple containing the minimum, maximum,
        and range of the dataset, as well as the cell size on the provided axis.
    """
    coordinate_min = np.min(coordinate_grid)
    coordinate_max = np.max(coordinate_grid)
    coordinate_range = coordinate_max - coordinate_min
    cell_size = coordinate_range / cell_count
    return (coordinate_min, coordinate_max, coordinate_range, cell_size)


def compute_coordinate_indecies(coordinate_min, coordinate_max, coordinate_cell_size):
    return np.arange(coordinate_min, coordinate_max, coordinate_cell_size)


def compute_coordinate_distance(lat_a, lon_a, lat_b, lon_b):
    return math.sqrt((abs(lat_a - lat_b) ** 2) + (abs(lon_a - lon_b) ** 2))


def compute_distance_from_coordinate_to_osom_grid(
    point_lat, point_lon, grid_lat, grid_lon
):
    """
    create 2d array the size of etiher grid_lat or grid_lon.
    then, naive loop to determine the distance using compute_coordinate_distance.
    take the value and put it in the output array.
    return the output array.
    """
    pass


if __name__ == "__main__":
    lat_len = 16
    lon_len = 26
    lat, lon, mask, bathymetry = import_grid("data/osom_grid.nc")
    lat_min, lat_max, lat_range, lat_cell_size = determine_bounds(lat, lat_len)
    lon_min, lon_max, lon_range, lon_cell_size = determine_bounds(lon, lon_len)
    lat_indecies = compute_coordinate_indecies(lat_min, lat_max, lat_cell_size)
    lon_indecies = compute_coordinate_indecies(lon_min, lon_max, lon_cell_size)
    print(lat_indecies, lon_indecies)
