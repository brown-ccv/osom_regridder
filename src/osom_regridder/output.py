import numpy as np
import netCDF4 as nc
from PIL import Image as img
from PIL.Image import Image
from typing import Tuple


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


def compute_normalization_scale(dataset: np.ndarray) -> Tuple[float, float]:
    """
    Determines the minimum and maximum values of the processed dataset.

    Parameters:
      dataset (np.ndarray): A regridded OSOM dataset presented as a 2D NumPy array.

    Returns:
      Tuple[float, float]: A tuple containing the minimum and maximum values of the dataset.
    """
    values = np.unique(dataset[~np.isnan(dataset)])
    return (np.min(values), np.max(values))


def create_image(dataset: np.ndarray, output_dim_x: int, output_dim_y: int) -> Image:
    """
    Transforms the dataset into a bitmap image. All NaN entries in the dataset are written as
    transparent pixels, and everything is normalized on a black -> purple color scale.
    """
    image = img.new(mode="RGBA", size=(output_dim_x, output_dim_y), color=(0, 0, 0, 0))
    output_min, output_max = compute_normalization_scale(dataset)
    for x in range(output_dim_x):
        for y in range(output_dim_y):
            value = dataset[x][y]
            if not np.isnan(value):
                color_as_value = int(
                    normalize_linear(value, output_min, output_max, 0, 255)
                )
                image.putpixel(
                    (x, output_dim_y - 1 - y), (color_as_value, 0, color_as_value, 255)
                )
    return image


def save_image(image: Image, image_path: str) -> None:
    """
    Utility function to write a create image to disk.

    Parameters:
      image (Image): Pillow Image object.
      image_path (string): Path where image will be saved.

    Returns:
        None: Image is written to disk.
    """
    image.save(image_path)


def save_dataset(dataset: np.ndarray, variable: str, file_path: str) -> None:
    """
    Utility function to write the dataset to disk as a NetCDF file.

    Parameters:
      dataset (np.ndarray): Regridded OSOM dataset.
      variable (str): Variable being saved in this NetCDF file.
      file_path (str): Path where the dataset will be written.

    Returns:
      None: Dataset is written to disk.
    """
    with nc.Dataset(file_path, "w") as output_file:
        output_file.createDimension("rows", dataset.shape[0])
        output_file.createDimension("cols", dataset.shape[1])
        data_var = output_file.createVariable(variable, "float32", ("rows", "cols"))
        data_var[:] = dataset
