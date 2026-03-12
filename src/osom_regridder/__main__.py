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

from .bounds import determine_bounds_for_dataset, determine_bounds_for_dir
from .constants import OSOMVariables, SurfaceOrBottom, default_height, default_width
from .file_input import import_grid, import_dataset, import_regridded_dataset
from .georeference import make_mbtile_for_dir
from .output import create_image, save_image, save_dataset_2d, save_dataset_3d
from .regrid import regrid_timepoint, regrid_dataset

app = typer.Typer(no_args_is_help=True)


@app.command()
def regrid_at_timepoint(
    grid_path: str,
    dataset_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
    surface_or_bottom: Annotated[
        SurfaceOrBottom, typer.Option()
    ] = SurfaceOrBottom.SURFACE,
    timepoint: Annotated[int, typer.Option(help="Timepoint in day (starting at midnight).")] = 1,
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
def regrid_to_image(
    regridded_data_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
    datatset_min: Annotated[float, typer.Option()] = -float('inf'),
    dataset_max: Annotated[float, typer.Option()] = float('inf'),
):
    dataset = import_regridded_dataset(regridded_data_path, variable)
    width, height = dataset.shape
    computed_min, computed_max = compute_dataset_bounds(dataset)
    image_min = computed_min if datatset_min == -float('inf') else datatset_min
    image_max = computed_max if datatset_max == -float('inf') else datatset_max

    image = create_image(dataset, width, height, variable, image_min, image_max)
    # Use the input path but rename to change the extension .tif
    output_path = Path("out/") / (Path(regridded_data_path).stem + ".tif")
    print("Saving regridded image to", output_path)
    save_image(image, output_path)


@app.command()
def regrid_to_images(
    regridded_data_path: str,
    datatset_min: float,
    dataset_max: float,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP,
):
    dataset = import_regridded_dataset(regridded_data_path, variable)
    timepoints, width, height = dataset.shape
    for timepoint in range(timepoints):
        image = create_image(
            dataset[timepoint], width, height, variable, datatset_min, dataset_max
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
