import netCDF4 as nc
from typing import Tuple


def import_grid(
    grid_path: str,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Extracts OSOM Grid data from a raw NC file.
    """
    osom_grid = nc.Dataset(grid_path)
    lat = osom_grid.variables["lat_rho"][:]
    lon = osom_grid.variables["lon_rho"][:]
    mask = osom_grid.variables["mask_rho"][:]
    bathymetry = osom_grid.variables["h"][:]
    return (lat, lon, mask, bathymetry)


def import_dataset(dataset_path: str) -> nc.Dataset:
    """
    Extracts data from a processed OSOM data file.
    """
    dataset = nc.Dataset(dataset_path)
    variable_id = f"{variable}{surface_or_bottom}"
    return dataset.variables[variable_id][:]


def import_regridded_dataset(dataset_path: str, variable: str) -> np.ndarray:
    dataset = nc.Dataset(dataset_path)
    return dataset.variables[variable][:]


if __name__ == "__main__":
    pass
