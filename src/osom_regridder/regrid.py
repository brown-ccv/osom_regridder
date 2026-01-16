"""
Module to regrid using scipy's griddata function

Functions:
  create_meshgrid: A helper function to create much used during interpolation.
  mask_data: A helper function to apply a mask prior to regridding.
  regrid: the function that performs the regridding.
"""

import numpy as np
from scipy.interpolate import griddata


def create_meshgrid(
    grid_size_x: int,
    grid_size_y: int,
    grid_bound_min_x: float,
    grid_bound_max_x: float,
    grid_bound_min_y: float,
    grid_bound_max_y: float,
):
    xi = np.linspace(grid_bound_min_x, grid_bound_max_x, grid_size_x)
    yi = np.linspace(grid_bound_min_y, grid_bound_max_y, grid_size_y)
    return np.meshgrid(xi, yi)


def mask_data(data: np.ndarray, mask: np.ndarray):
    return np.where(mask, data, np.nan)


def grid_transform(
    lon2d: np.ndarray,
    lat2d: np.ndarray,
    data2d: np.ndarray,
    meshgrid: tuple[np.ndarray, np.ndarray],
    mask: np.ndarray,
):
    return griddata((lon2d.flatten(), lat2d.flatten()), data2d.flatten(), meshgrid)
