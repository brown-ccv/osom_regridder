import numpy as np
import netCDF4 as nc
import cmocean
import math

from PIL import Image as img
from PIL.Image import Image

from typing import Tuple
from .utils import compute_dataset_bounds, normalize_linear
from .constants import OSOMVariables


def get_colormap(cm_name: str):
    if cm_name == "thermal":
        return cmocean.cm.thermal
    elif cm_name == "haline":
        return cmocean.cm.haline
    elif cm_name == "solar":
        return cmocean.cm.solar
    elif cm_name == "ice":
        return cmocean.cm.ice
    elif cm_name == "gray":
        return cmocean.cm.gray
    elif cm_name == "oxy":
        return cmocean.cm.oxy
    elif cm_name == "deep":
        return cmocean.cm.deep
    elif cm_name == "dense":
        return cmocean.cm.dense
    elif cm_name == "algae":
        return cmocean.cm.algae
    elif cm_name == "matter":
        return cmocean.cm.matter
    elif cm_name == "turbid":
        return cmocean.cm.turbid
    elif cm_name == "speed":
        return cmocean.cm.speed
    elif cm_name == "amp":
        return cmocean.cm.amp
    elif cm_name == "tempo":
        return cmocean.cm.tempo
    elif cm_name == "rain":
        return cmocean.cm.rain
    elif cm_name == "phase":
        return cmocean.cm.phase
    elif cm_name == "topo":
        return cmocean.cm.topo
    elif cm_name == "balance":
        return cmocean.cm.balance
    elif cm_name == "delta":
        return cmocean.cm.delta
    elif cm_name == "curl":
        return cmocean.cm.curl
    elif cm_name == "diff":
        return cmocean.cm.diff
    elif cm_name == "tarn":
        return cmocean.cm.tarn
    else:
        return cmocean.cm.thermal


def get_colormap_for_variable(variable: str):
    if variable == OSOMVariables.TEMP:
        return cmocean.cm.thermal
    if variable == OSOMVariables.SALT:
        return cmocean.cm.haline
    # if variable == OSOMVariables.ZETA:
    #    pass
    if variable == OSOMVariables.KINETIC_ENERGY:
        return cmocean.cm.speed
    if variable == OSOMVariables.UBAR_EAST:
        return cmocean.cm.dense
    if variable == OSOMVariables.UBAR_WEST:
        return cmocean.cm.dense
    if variable == "bathymetry":
        return cmocean.cm.deep
    # Default to the Ice colormap.
    return cmocean.cm.ice


def create_image(
    dataset: np.ndarray,
    output_dim_x: int,
    output_dim_y: int,
    variable: str,
    visualization_min: float,
    visualization_max: float,
) -> Image:
    """
    Transforms the dataset into a bitmap image. All NaN entries in the dataset are written as
    transparent pixels, and everything is normalized on a black -> purple color scale.
    """
    image = img.new(mode="RGBA", size=(output_dim_x, output_dim_y), color=(0, 0, 0, 0))
    cmap = get_colormap_for_variable(variable)
    # cmap = get_colormap(cm_name)
    for x in range(output_dim_x):
        for y in range(output_dim_y):
            value = dataset[x][y]
            if not np.isnan(value):
                normalized_value = normalize_linear(
                    value, visualization_min, visualization_max, 0, 1
                )
                r, g, b, a = cmap(normalized_value)
                image.putpixel(
                    (x, output_dim_y - 1 - y),
                    (
                        math.floor(r * 255),
                        math.floor(g * 255),
                        math.floor(b * 255),
                        128,
                    ),
                )
    return image.transpose(img.ROTATE_270)


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


def save_dataset_2d(dataset: np.ndarray, variable: str, file_path: str) -> None:
    """
    Utility function to write a 2d dataset to disk as a NetCDF file.

    Parameters:
      dataset (np.ndarray): Regridded OSOM dataset.
      variable (str): Variable being saved in this NetCDF file.
      file_path (str): Path where the dataset will be written.

    Returns:
      None: Dataset is written to disk.
    """
    with nc.Dataset(file_path, "w") as output_file:
        output_file.createDimension("lat", dataset.shape[0])
        output_file.createDimension("lon", dataset.shape[1])
        data_var = output_file.createVariable(variable, "float32", ("lat", "lon"))
        data_var[:] = dataset


def save_dataset_3d(dataset: np.ndarray, variable: str, file_path: str) -> None:
    """
    Utility function to write a 3d dataset (regridded at each timepoint) to disk as a NetCDF file.

    Parameters:
      dataset (np.ndarray): Regridded OSOM dataset.
      variable (str): Variable being saved in this NetCDF file.
      file_path (str): Path where the dataset will be written.

    Returns:
      None: Dataset is written to disk.
    """
    with nc.Dataset(file_path, "w") as output_file:
        output_file.createDimension("time", dataset.shape[0])
        output_file.createDimension("lat", dataset.shape[1])
        output_file.createDimension("lon", dataset.shape[2])
        data_var = output_file.createVariable(
            variable, "float32", ("time", "lat", "lon")
        )
        data_var[:] = dataset
