"""
Module to regrid using scipy's griddata function

Functions:
  create_meshgrid: A helper function to create a meshgrid used during interpolation.
  mask_data: A helper function to apply a mask prior to regridding.
  grid_transform: Transforms dataset data onto output grid.
  regrid_at_timepoint: Pipeline function to regrid data at a timepoint.

"""

import numpy as np
from scipy.interpolate import griddata
import time

from .constants import LON_W, LON_E, LAT_N, LAT_S


def create_meshgrid(
    grid_size_x: int,
    grid_size_y: int,
    grid_bound_min_x: float,
    grid_bound_max_x: float,
    grid_bound_min_y: float,
    grid_bound_max_y: float,
) -> tuple[np.ndarray, np.ndarray]:
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


def regrid_timepoint(
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    dataset: np.ndarray,
    dimensions: tuple[int, int],
    timepoint: int,
):
    lat, lon, mask, bathymetry = grid
    width, height = dimensions
    meshgrid = create_meshgrid(width, height, LON_W, LON_E, LAT_N, LAT_S)
    data_at_timepoint = dataset[timepoint]
    regridded_data = grid_transform(lon, lat, data_at_timepoint, meshgrid, mask)
    return regridded_data


def regrid_dataset(
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    dataset: np.ndarray,
    dimensions: tuple[int, int],
):
    """ """
    lat, lon, mask, bathymetry = grid
    width, height = dimensions
    meshgrid = create_meshgrid(width, height, LON_W, LON_E, LAT_N, LAT_S)
    timepoints = dataset.shape[0]
    output_dataset = np.zeros((timepoints, height, width))
    start = time.time()
    for timepoint in range(timepoints):
        regridded_data = grid_transform(lon, lat, dataset[timepoint], meshgrid, mask)
        output_dataset[timepoint] = regridded_data
        print(f"{timepoint + 1}/{timepoints}")
    print(f"Finished in {time.time() - start}")
    return output_dataset
