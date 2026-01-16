"""
The command line interface for the OSOM regridding tool.

Commands:
 - regrid: Runs the regridding algorithm on a given file.
 - display: Creates a PNG based on regridded data.
 - tile: Creates a .mbtiles file from regridded data. Not yet implemented.

"""

import typer
from enum import Enum
from pathlib import Path
from typing_extensions import Annotated

from .file_input import import_grid, import_dataset, import_regridded_dataset
from .regrid import create_meshgrid, grid_transform, regrid_timepoint, regrid_dataset

# from .regrid import populate_regrid
from .output import create_image, save_image, save_dataset_2d, save_dataset_3d
# from .compute_map import (
#    determine_bounds,
#    compute_coordinate_indecies,
#    compute_distance_from_coordinate_to_osom_grid,
#    get_distances_below_threshold,
#    compute_cell_sizes,
# )

# from .map_interface import (
#    initialize_grid,
#    close,
#    save_distances,
#    save_sizes,
#    load_grid,
#    get_distances,
# )

app = typer.Typer(no_args_is_help=True)


default_height = 160
default_width = 260
# default_distance_threshold = 0.3


class OSOMVariables(str, Enum):
    TEMP = "temp"
    SALT = "salt"
    ZETA = "zeta"
    UBAR_EAST = "ubar_eastward"
    UBAR_WEST = "ubar_westward"


class SurfaceOrBottom(str, Enum):
    SURFACE = "surface"
    BOTTOM = "bottom"


# @app.command()
# def regrid(
#    grid_path: str,
#    dataset_path: str,
#    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
#    surfaceOrBottom: Annotated[
#        SurfaceOrBottom, typer.Option()
#    ] = SurfaceOrBottom.SURFACE,
#    timepoint: Annotated[int, typer.Option(help="Days since model inception.")] = 1,
#    height: Annotated[int, typer.Option()] = default_height,
#    width: Annotated[int, typer.Option()] = default_width,
# ):
#    lat, lon, mask, bathymetry = import_grid(grid_path)
#    data = import_dataset(dataset_path, variable.value, surfaceOrBottom.value)
#    data_at_timepoint = data[timepoint]
#    regridded = populate_regrid(width, height, lon, lat, data_at_timepoint)
#    # Use the input path but add variable and timepoint ID.
#    output_path = Path("out/") / (
#        Path(dataset_path).stem + f"_{variable.value}@{timepoint}.nc"
#    )
#    print("Saving regridded dataset to", output_path)
#    save_dataset(regridded, variable, output_path)


# @app.command()
# def regrid(
#   grid_path: str,
#    dataset_path: str,
#    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
#    surface_or_bottom: Annotated[
#        SurfaceOrBottom, typer.Option()
#    ] = SurfaceOrBottom.SURFACE,
#    timepoint: Annotated[int, typer.Option(help="Days since model inception.")] = 1,
#    height: Annotated[int, typer.Option()] = default_height,
#    width: Annotated[int, typer.Option()] = default_width,
# ):
#    lat, lon, mask, bathymetry = import_grid(grid_path)
#   data_at_timepoint = data[timepoint]
#    meshgrid = create_meshgrid(width, height, LON_W, LON_E, LAT_N, LAT_S)
#    regridded = grid_transform(lon, lat, data_at_timepoint, meshgrid, mask)
#    # Use the input path but add variable and timepoint ID.
#    output_path = Path("out/") / (
#        Path(dataset_path).stem + f"_{variable.value}@{timepoint}.nc"
#    )
#    print("Saving regridded dataset to", output_path)
#    save_dataset(regridded, variable, output_path)


@app.command()
def regrid_at_timepoint(
    grid_path: str,
    dataset_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
    surface_or_bottom: Annotated[
        SurfaceOrBottom, typer.Option()
    ] = SurfaceOrBottom.SURFACE,
    timepoint: Annotated[int, typer.Option(help="Days since model inception.")] = 1,
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
):
    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path, variable.value, surface_or_bottom.value)
    regridded = regrid_timepoint(grid, dataset, (width, height), timepoint)

    output_path = Path("out/") / (
        Path(dataset_path).stem + f"_{variable.value}@{timepoint}.nc"
    )
    print("Saving regridded dataset to", output_path)
    save_dataset_2d(regridded, variable, output_path)


@app.command()
def regrid(
    grid_path: str,
    dataset_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
    surface_or_bottom: Annotated[
        SurfaceOrBottom, typer.Option()
    ] = SurfaceOrBottom.SURFACE,
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
):
    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path, variable.value, surface_or_bottom.value)
    regridded = regrid_dataset(grid, dataset, (width, height))

    output_path = Path("out/") / (Path(dataset_path).stem + f"_{variable.value}.nc")
    print("Saving regridded dataset to", output_path)
    save_dataset_3d(regridded, variable.value, output_path)


@app.command()
def tile():
    raise NotImplementedError("Not Implemented.")


@app.command()
def display(regridded_data_path: str, variable: str):
    dataset = import_regridded_dataset(regridded_data_path, variable)
    width, height = dataset.shape
    image = create_image(dataset, width, height)
    # Use the input path but rename to change the extension .png
    output_path = Path("out/") / (Path(regridded_data_path).stem + ".png")
    print("Saving regridded image to", output_path)
    save_image(image, output_path)


# @app.command()
# def map(
#    grid_path: str,
#    height: Annotated[int, typer.Option()] = default_height,
#    width: Annotated[int, typer.Option()] = default_width,
##    threshold: Annotated[int, typer.Option()] = default_distance_threshold,
# ):
#    lat, lon, mask, bathymetry = import_grid(grid_path)
#    lat_min, lat_max, lat_range, lat_cell_size = determine_bounds(lat, height)
#    lon_min, lon_max, lon_range, lon_cell_size = determine_bounds(lon, width)
#    lat_indecies = compute_coordinate_indecies(lat_min, lat_max, lat_cell_size)
#    lon_indecies = compute_coordinate_indecies(lon_min, lon_max, lon_cell_size)
#    sizes, sizes_grid = compute_cell_sizes(lat, lon)
#    lat_one = lat_indecies[0]
#    lon_one = lon_indecies[0]
#    distances = compute_distance_from_coordinate_to_osom_grid(
#        lat_one, lon_one, lat, lon
#    )
#    selected_distances = get_distances_below_threshold(distances, threshold)
#    grid_path = Path("out/") / f"remap_grid_{height}x{width}~{threshold}.sqlite"
#    grid = initialize_grid(grid_path)
#    save_distances(grid, 0, 0, selected_distances)
#    save_sizes(grid, sizes)
#    close(grid)
#    loaded_grid = load_grid(grid_path)
#    query_result = get_distances(loaded_grid, 0, 0)
#    print(query_result)
#    close(grid)


if __name__ == "__main__":
    app()
