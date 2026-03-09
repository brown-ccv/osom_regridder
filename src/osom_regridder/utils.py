import numpy as np


def compute_dataset_bounds(dataset: np.ndarray) -> Tuple[float, float]:
    """
    Determines the minimum and maximum values of the processed dataset.

    Parameters:
      dataset (np.ndarray): A regridded OSOM dataset presented as a 2D NumPy array.

    Returns:
      Tuple[float, float]: A tuple containing the minimum and maximum values of the dataset.
    """
    return (np.nanmin(dataset), np.nanmax(dataset))


def normalize_linear(
    value: float,
    input_scale_min: float,
    input_scale_max: float,
    output_scale_min: float,
    output_scale_max: float,
) -> float:
    """
    Utility function to linearly normalize model data for the creation of output images.

    Parameters:
        value (float): The value to be normalized.
        input_scale_min (float): The minimum value of the input range.
        input_scale_max (float): The maximum value of the input range.
        output_scale_min (float): The minimum value of the output range.
        output_scale_max (float): The maximum value of the output range.

    Returns:
        float: The normalized value scaled to the output range.
    """
    standard_normalization = (value - input_scale_min) / (
        input_scale_max - input_scale_min
    )
    return (
        (output_scale_max - output_scale_min) * standard_normalization
    ) + output_scale_min
