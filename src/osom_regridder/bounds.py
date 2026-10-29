import numpy as np
from time import time
from pathlib import Path

from .file_input import import_dataset
from .utils import compute_dataset_bounds


def determine_bounds_for_dataset(dataset_path: str, variable: str):
    dataset = import_dataset(dataset_path)
    return compute_dataset_bounds(dataset.variables[variable])


def determine_bounds_for_collection(dataset_dir: str, variable: str):
    collection_min = np.inf
    collection_max = -1 * np.inf
    datasets = list(Path(dataset_dir).iterdir())
    for dataset in datasets:
        dataset_min, dataset_max = determine_bounds_for_dataset(dataset, variable)
        if dataset_min < collection_min:
            collection_min = dataset_min
        if dataset_max > collection_max:
            collection_max = dataset_max
    return collection_min, collection_max
