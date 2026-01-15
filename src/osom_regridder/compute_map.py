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


def compute_coordinate_indecies(
    coordinate_min: float, coordinate_max: float, coordinate_cell_size: float
) -> np.ndarray:
    """
    Helper function to get a lon/lat coordinate at each grid index.
    """
    return np.arange(coordinate_min, coordinate_max, coordinate_cell_size)


def compute_coordinate_distance(
    lat_a: float, lon_a: float, lat_b: float, lon_b: float
) -> float:
    """
    Helper function to compute cartesian distance between two lon/lat points.
    """
    return math.sqrt((abs(lat_a - lat_b) ** 2) + (abs(lon_a - lon_b) ** 2))


def compute_distance_from_coordinate_to_osom_grid(
    point_lat: float, point_lon: float, grid_lat: np.ndarray, grid_lon: np.ndarray
) -> np.ndarray:
    """
    create 2d array the size of etiher grid_lat or grid_lon.
    then, naive loop to determine the distance using compute_coordinate_distance.
    take the value and put it in the output array.
    return the output array.
    """
    x, y = grid_lat.shape
    distances = np.zeros((x, y))
    for x_idx in range(x):
        for y_idx in range(y):
            i_lat = grid_lat[x_idx][y_idx]
            i_lon = grid_lon[x_idx][y_idx]
            distance = compute_coordinate_distance(point_lat, point_lon, i_lat, i_lon)
            distances[x_idx][y_idx] = distance
    return distances


def get_distances_below_threshold(distance_grid: np.ndarray, threshold: float):
    x_idxs, y_idxs = np.where(distance_grid < threshold)
    indecies_with_distances = np.zeros((len(x_idxs), 3))
    for idx in range(len(x_idxs)):
        x = x_idxs[idx]
        y = y_idxs[idx]
        distance = distance_grid[x][y]
        indecies_with_distances[idx] = (x, y, distance)
    return indecies_with_distances


def compute_cell_sizes(lat_grid: np.ndarray, lon_grid: np.ndarray):
    sizes_grid = np.zeros(lat_grid.shape)
    cell_sizes = []
    x_range, y_range = lon_grid.shape
    for x in range(x_range):
        for y in range(y_range):
            y_next = y - 1 if y == y_range - 1 else y + 1
            x_next = x - 1 if x == x_range - 1 else x + 1
            width = Math.abs(lat_grid[x][y] - lat_grid[x_next][y])
            height = Math.abs(lon_grid[x][y] - lon_grid[x][y_next])
            size =  (width + height) / 2
            cell_sizes.append((x, y, width, height, size))
            sizes_grid[x][y] = (width, height, size)
    return cell_sizes, sizes_grid


def compute_distance_threshold(distance_grid: np.ndarray, sizes: np.ndarray):
    # algorithm:
    # given x, y, find the width/heigh of the input grid cell. 
    # find the max and min sizes for the whole grid
    # linearly interpolate with size of the selected cell onto [0.5,1.5] scale
    # multiple the height of the selected grid cell by the interpolated coefficient
    # select all distance values less than the selected coefficient
    x, y, min_distance = distance_grid[np.argmin(distance_grid[:,2])]
    min_size = np.min(npsizes[:,4])
    max_size = np.max(npsizes[:,4])
    
    



if __name__ == "__main__":
    lat_len = 16
    lon_len = 26
    lat, lon, mask, bathymetry = import_grid("data/osom_grid.nc")
    lat_min, lat_max, lat_range, lat_cell_size = determine_bounds(lat, lat_len)
    lon_min, lon_max, lon_range, lon_cell_size = determine_bounds(lon, lon_len)
    lat_indecies = compute_coordinate_indecies(lat_min, lat_max, lat_cell_size)
    lon_indecies = compute_coordinate_indecies(lon_min, lon_max, lon_cell_size)
    print(lat_indecies, lon_indecies)
