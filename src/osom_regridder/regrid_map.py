"""
Module to regrid using a regrid map

Functions:
  regrid: main interface function to perform a regird operation given data and a grid.
  compute_output_point: determines the output value at a point based on input data and distances.
  weighted_average: utility function to average values by weight (distance)
"""

import numpy as np
import sqlite3

from .file_input import import_dataset
from .map_interface import load_grid, get_distances, close


def regrid(
    dataset_path: str,
    grid_path: str,
    height: int,
    width: int,
    variable: str,
    surfaceOrBottom: str,
):
    dataset = import_dataset(dataset_path, variable, surfaceOrBottom)
    grid_connection = load_grid(grid_path)
    output_dataset = np.zeros((width, height))
    for x in range(width):
        for y in range(height):
            output_dataset[x, y] = compute_output_point(grid_connection, x, y, dataset)
    close(grid_connection)
    return output_dataset


def compute_output_point(
    grid_connection: sqlite3.Connection,
    output_x: int,
    output_y: int,
    dataset: np.ndarray,
):
    distances = get_distances(connection, output_x, output_y)
    distance_data_pairs = []
    for dx, dy, distance in distances:
        value = dataset[dx][dy]
        pairs.append((distance, value))
    if len(distance_data_pairs) == 0:
        return np.nan
    return weighted_average(distance_data_pairs)


def weighted_average(points: tuple[float, float]) -> float:
    """
    points given (distance, value)
    """
    # https://en.wikipedia.org/wiki/Weighted_arithmetic_mean#Mathematical_definition
    # squares = [x**2 for x in range(10)]
    total_distance = np.sum([distance for distance, value in points])
    return np.sum([(distance / total_distance) * value for distance, value in points])


if __name__ == "__main__":
    pass
