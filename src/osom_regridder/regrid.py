"""
Module to regrid using scipy's griddata function

Functions:
  create_meshgrid: A helper function to create a meshgrid used during interpolation.
  mask_data: A helper function to apply a mask prior to regridding.
  grid_transform: Transforms dataset data onto output grid.
  regrid_timepoint: Pipeline function to regrid data at a timepoint.

"""

import netCDF4 as nc
import numpy as np
from scipy.interpolate import griddata

from .constants import LON_W, LON_E, LAT_N, LAT_S
from .utils import compute_timepoint_from_datetime


def create_meshgrid(
    grid_size_x: int,
    grid_size_y: int,
    grid_bound_min_x: float,
    grid_bound_max_x: float,
    grid_bound_min_y: float,
    grid_bound_max_y: float,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Helper function to create a meshgrid used during interpolation.

    Parameters:
        grid_size_x (int): Mesh size in X (longitude) dimension.
        grid_size_y (int): Mesh size in Y (latitude) dimension.
        grid_bound_min_x (float): Minimum X (longitude) bound.
        grid_bound_max_x (float): Maximum X (longitude) bound.
        grid_bound_min_y (float): Minimum Y (latitude) bound.
        grid_bound_max_y (float): Maximum Y (latitude) bound.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple of arrays representing the full output space.
    """
    xi = np.linspace(grid_bound_min_x, grid_bound_max_x, grid_size_x)
    yi = np.linspace(grid_bound_min_y, grid_bound_max_y, grid_size_y)
    return np.meshgrid(xi, yi)


def mask_data(data: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """
    Helper function to apply a mask to data prior to regridding.

    Parameters:
        data (np.ndarray): Raw dataset.
        mask (np.ndarray): Mask being applied.

    Returns:
        np.ndarray: Data with mask applied.
    """
    return np.where(mask, data, np.nan)


def grid_transform(
    lon2d: np.ndarray,
    lat2d: np.ndarray,
    data2d: np.ndarray,
    meshgrid: tuple[np.ndarray, np.ndarray],
    mask: np.ndarray,
):
    """
    Function to apply regrid transformation to the dataset.

    Parameters:
        lon2d (np.ndarray): 2D array of Longitude points in the input dataset.
        lat2d (np.ndarray): 2D array of Latitude points in the input dataset.
        data2d (np.ndarray): 2D array of data to be regridded.
        meshgrid (tuple[np.ndarray, np.ndarray]): A meshgrid of the desired output size. See: create_meshgrid
        mask (np.ndarray): A mask to be applied to the dataset prior to regridding.

    Returns:
        np.ndarray: Regridded data matching the shape of the meshgrid.
    """
    return griddata(
        (lon2d.flatten(), lat2d.flatten()),
        mask_data(data2d, mask).flatten(),
        meshgrid,
        method="linear",
    )


def regrid_timepoint(
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    dataset: nc.Dataset,
    variable: str,
    surface_or_bottom: str,
    dimensions: tuple[int, int],
    timepoint: int,
) -> np.ndarray:
    """
    Helper function to regrid a dataset at a specific timepoint.

    Parameters:
        grid (tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]): Grid information -- output of file_input.import_grid
        dataset (np.ndarray): Dataset to be processed.
        variable (str): Variable being regridded.
        surface_or_bottom (str): Variable depth (combined with `variable`).
        dimensions (tuple[int, int]): Output dimensions in width (longitude) / height (latitude)
        timepoint (int): Timepoint to be processed (index into processed dataset)

    Returns:
        np.ndarray: Regridded dataset.
    """
    lat, lon, mask, bathymetry = grid
    width, height = dimensions
    meshgrid = create_meshgrid(width, height, LON_W, LON_E, LAT_N, LAT_S)
    data_at_timepoint = dataset.variable[f"{variable}{surface_or_bottom}"][timepoint]
    regridded_data = grid_transform(lon, lat, data_at_timepoint, meshgrid, mask)
    return regridded_data


def regrid_dataset(
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    dataset: np.ndarray,
    dimensions: tuple[int, int],
) -> np.ndarray:
    """
    Helper function to regrid an entire dataset

    Parameters:
        grid (tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]): Grid information -- output of file_input.import_grid
        dataset (np.ndarray): Dataset to be processed.
        dimensions (tuple[int, int]): Output dimensions in width (longitude) / height (latitude)

    Returns:
        np.ndarray: Regridded dataset at all timepoints.
    """
    lat, lon, mask, bathymetry = grid
    width, height = dimensions
    meshgrid = create_meshgrid(width, height, LON_W, LON_E, LAT_N, LAT_S)
    timepoints = dataset.shape[0]
    output_dataset = np.zeros((timepoints, height, width))
    for timepoint in range(timepoints):
        regridded_data = grid_transform(lon, lat, dataset[timepoint], meshgrid, mask)
        output_dataset[timepoint] = regridded_data
    return output_dataset


def batch_regrid(
    grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    dataset: nc.Dataset,
    variables: list[str],
    timepoints: list[str],
    dimensions: tuple[int, int],
) -> dict[str, dict[str, np.ndarray]]:
    """
    Helper function to regrid a dataset for a given set of variables and timepoints.

    Parameters:
        grid (tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]): Grid information -- output of file_input.import_grid
        dataset (np.ndarray): Dataset to be processed.
        varaibles (list[str]): List of variables to process timepoints for.
        timepoints (list[str]): List of timepoints in ISO format to be regridded.
        dimensions (tuple[int, int]): Output dimensions in width (longitude) / height (latitude)

    Returns:
        dict[str, dict[str, np.ndarray]]: Nested dictionaries containing variable and timestamp information for seperate regrids
    """
    lat, lon, mask, bathymetry = grid
    width, height = dimensions
    meshgrid = create_meshgrid(width, height, LON_W, LON_E, LAT_N, LAT_S)
    # Note (AM): There's a chance this might be more performant if you pre-allocate
    # an ndarray and return it alongside a python list of variable / timepoint pairs,
    # such that metadata[index] and regridded_data[index] gave you metadata and data
    # for each regrid.
    regridded_data = {}
    for variable in variables:
        data_for_variable = dataset.variables[variable]
        regridded_data[variable] = {}
        for timepoint in timepoints:
            index = compute_timepoint_from_datetime(timepoint)
            regridded_data[variable][timepoint] = grid_transform(
                lon, lat, data_for_variable[index], meshgrid, mask
            )
    return regridded_data
