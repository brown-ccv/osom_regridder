import numpy as np
from time import time
from pathlib import Path

from .file_input import import_dataset
from .utils import compute_dataset_bounds


def determine_bounds_for_dataset(
    dataset_path: str, variable: str, surface_or_bottom: str
):
    dataset = import_dataset(dataset_path, variable, surface_or_bottom)
    return compute_dataset_bounds(dataset)


def determine_bounds_for_dir(dataset_dir: str, variable: str, surface_or_bottom: str):
    dir_min = np.inf
    dir_max = -1 * np.inf
    for dataset_path in Path(dataset_dir).iterdir():
        if dataset_path.is_file():
            dataset_min, dataset_max = determine_bounds_for_dataset(
                dataset_path, variable, surface_or_bottom
            )
            if dataset_min < dir_min:
                dir_min = dataset_min
            if dataset_max < dir_max:
                dir_max = dataset_max
    return dir_min, dir_max
