import datetime as dt
import numpy as np


def compute_dataset_bounds(dataset: np.ndarray) -> tuple[float, float]:
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


def compute_timepoint_from_datetime(timestamp: str):
    """
    Utility function that will determine the number of 1.5
    hour timesteps a given timestamp is from the start of
    the year in which the timestamp occurred.

    Parameters:
        timestmp (dt.dateime): Timestamp under transformation

    Returns:
        int: The number of timesteps since the new year.
    """
    parsed_timestamp = dt.datetime.fromisoformat(timestamp)
    delta_since_new_year = parsed_timestamp - dt.datetime.fromisoformat(
        f"{parsed_timestamp.year}-01-01T00:00"
    )
    # Each day contains 16 timesteps. Add this with the number of
    # hours in the remaining day divided by 1.5 (rounded) to
    # determine the number of timesteps in the delta.
    timestep = (delta_since_new_year.days * 16) + round(
        delta_since_new_year.seconds / (60 * 60) / 1.5
    )
    return timestep
