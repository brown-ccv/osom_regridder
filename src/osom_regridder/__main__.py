"""
The command line interface for the OSOM regridding tool.

Commands:
 - regrid: Runs the regridding algorithm on a given file.
 - display: Creates a TIF based on regridded data.
 - tile: Creates a .mbtiles file from regridded data. Not yet implemented.

"""

import typer
from pathlib import Path
from typing_extensions import Annotated
import os
import datetime as dt

from .bounds import determine_bounds_for_dataset, determine_bounds_for_dir
from .constants import OSOMVariables, SurfaceOrBottom, default_height, default_width
from .file_input import (
    import_grid,
    import_dataset,
    import_regridded_dataset,
)
from .georeference import make_mbtile_for_dir
from .output import create_image, save_image, save_dataset_2d, save_dataset_3d
from .regrid import regrid_timepoint, regrid_dataset, do_batch_regrid
from .utils import compute_timepoint_from_datetime

app = typer.Typer(no_args_is_help=True)


@app.command()
def regrid_at_timepoint(
    grid_path: str,
    dataset_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
    surface_or_bottom: Annotated[
        SurfaceOrBottom, typer.Option()
    ] = SurfaceOrBottom.SURFACE,
    timepoint: Annotated[
        str, typer.Option(help="ISO String for the timepoint you want to regrid.")
    ] = "2005-01-01T00:00",
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
):
    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path, variable.value, surface_or_bottom.value)
    regridded = regrid_timepoint(
        grid,
        dataset.variables[f"{variable}{surface_or_bottom}"],
        (width, height),
        compute_timepoint_from_datetime(dt.datetime.fromisoformat(timepoint)),
    )

    output_path = Path("out/") / (
        Path(dataset_path).stem + f"_{variable.value}@{timepoint}.nc"
    )
    print("Saving regridded dataset to", output_path)
    save_dataset_2d(regridded, variable, output_path)


# @app.command()
# def regrid(
#    grid_path: str,
#    dataset_path: str,
#    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
#    surface_or_bottom: Annotated[
#        SurfaceOrBottom, typer.Option()
#    ] = SurfaceOrBottom.SURFACE,
#    height: Annotated[int, typer.Option()] = default_height,
#    width: Annotated[int, typer.Option()] = default_width,
# ):
#    grid = import_grid(grid_path)
#    dataset = import_dataset(dataset_path)
#    regridded = regrid_dataset(grid, dataset, (width, height))

#    output_path = Path("out/") / (Path(dataset_path).stem + f"_{variable.value}.nc")
#    print("Saving regridded dataset to", output_path)
#    save_dataset_3d(regridded, variable.value, output_path)


@app.command()
def batch_regrid(
    grid_path: str,
    dataset_path: str,
    variables: str,
    timepoints: str,
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
):
    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path)
    variables_list = variables.split(",")
    timepoints_list = timepoints.split(",")
    regrid = do_batch_regrid(
        grid, dataset, variables_list, timepoints_list, (width, height)
    )
    for variable in variables_list:
        for timepoint in timepoints_list:
            output_path = Path("out/") / (
                Path(dataset_path).stem + f"_{variable}@{timepoint}.nc"
            )
            print("Saving regridded dataset to", output_path)
            regridded = regrid[variable][timepoint]
            save_dataset_2d(regridded, variable, output_path)


@app.command()
def regrid_to_image(
    regridded_data_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
    dataset_min: Annotated[float, typer.Option()] = -float("inf"),
    dataset_max: Annotated[float, typer.Option()] = float("inf"),
):
    dataset = import_regridded_dataset(regridded_data_path, variable)
    width, height = dataset.shape
    # computed_min, computed_max = compute_dataset_bounds(dataset)
    image_min = (
        dataset_min  # computed_min if dataset_min == -float('inf') else dataset_min
    )
    image_max = (
        dataset_max  # computed_max if dataset_max == -float('inf') else dataset_max
    )

    image = create_image(dataset, width, height, variable, image_min, image_max)
    # Use the input path but rename to change the extension .tif
    output_path = Path("out/") / (Path(regridded_data_path).stem + ".tif")
    print("Saving regridded image to", output_path)
    save_image(image, output_path)


@app.command()
def regrid_to_images(
    regridded_data_path: str,
    dataset_min: float,
    dataset_max: float,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
):
    dataset = import_regridded_dataset(regridded_data_path, variable)
    timepoints, width, height = dataset.shape
    for timepoint in range(timepoints):
        image = create_image(
            dataset[timepoint], width, height, variable, dataset_min, dataset_max
        )
        output_path = Path("out/") / (
            Path(regridded_data_path).stem + f"@{timepoint}.tif"
        )
        save_image(image, output_path)
    print("Saved", timepoints, "images.")


@app.command()
def georef_dir(src: str, dst: str):
    if not os.path.exists(dst):
        os.mkdir(dst)
    make_mbtile_for_dir(src, dst)


@app.command()
def compute_dataset_bounds(
    dataset_path_or_dir: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
    surface_or_bottom: Annotated[
        SurfaceOrBottom, typer.Option()
    ] = SurfaceOrBottom.SURFACE,
):
    if not os.path.exists(dataset_path_or_dir):
        raise f"Path {dataset_path_or_dir} does not exist"
    if os.path.isdir(dataset_path_or_dir):
        dir_min, dir_max = determine_bounds_for_dir(
            dataset_path_or_dir, variable, surface_or_bottom
        )
        print(dir_min, dir_max)
    elif os.path.isfile(dataset_path_or_dir):
        dataset_min, dataset_max = determine_bounds_for_dataset(
            dataset_path_or_dir, variable, surface_or_bottom
        )
        print(dataset_min, dataset_max)


if __name__ == "__main__":
    app()
