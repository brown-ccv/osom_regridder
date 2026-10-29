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

from .bounds import determine_bounds_for_dataset, determine_bounds_for_collection
from .constants import (
    OSOMVariables,
    default_height,
    default_width,
    default_write_path,
    ALL_VARIABLES,
)
from .file_input import (
    import_grid,
    import_dataset,
    import_regridded_dataset,
)
from .georeference import make_mbtile_for_dir
from .output import create_image, save_image, save_dataset_2d, save_dataset_3d, save_gif
from .regrid import regrid_timepoint, regrid_data, do_batch_regrid, blur_timerange
from .utils import compute_timepoint_from_datestring, compute_dataset_bounds

app = typer.Typer(no_args_is_help=True)


@app.command()
def regrid(
    grid_path: str,
    dataset_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.SALINITY_BOTTOM,
    timepoint: Annotated[
        str, typer.Option(help="ISO String for the timepoint you want to regrid.")
    ] = "2005-01-01T00:00",
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
    out: Annotated[str, typer.Option()] = default_write_path,
):
    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path)
    regridded = regrid_timepoint(
        grid,
        dataset,
        variable.value,
        (width, height),
        compute_timepoint_from_datestring(timepoint),
    )

    output_path = Path(out) / (
        Path(dataset_path).stem + f"_{variable.value}@{timepoint}.nc"
    )
    print("Saving regridded dataset to", output_path)
    save_dataset_2d(regridded, variable, output_path)


@app.command()
def batch_regrid(
    grid_path: str,
    dataset_path: str,
    timepoints: Annotated[list[str], typer.Argument(help="Timepoints to regrid")],
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
    out: Annotated[str, typer.Option()] = default_write_path,
):
    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path)
    regrid = do_batch_regrid(
        grid,
        dataset,
        [variable.value for variable in ALL_VARIABLES],
        timepoints,
        (width, height),
    )
    for variable in ALL_VARIABLES:
        for timepoint in timepoints:
            output_path = Path(out) / (
                Path(dataset_path).stem + f"_{variable.value}@{timepoint}.nc"
            )
            print("Saving regridded dataset to", output_path)
            regridded = regrid[variable.value][timepoint]
            save_dataset_2d(regridded, variable.value, output_path)


@app.command()
def aggregate_regrid(
    grid_path: str,
    dataset_path: str,
    start: str,
    stop: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.SALINITY_BOTTOM,
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
    out: Annotated[str, typer.Option()] = default_write_path,
):
    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path)
    aggregate_data = blur_timerange(dataset, variable.value, start, stop)
    regridded_aggregate = regrid_data(grid, aggregate_data, (width, height))

    output_path = Path(out) / (
        Path(dataset_path).stem + f"_{variable.value}@{start}-{stop}.nc"
    )
    print("Saving regridded dataset aggregation to", output_path)
    save_dataset_2d(regridded_aggregate, variable, output_path)


@app.command()
def aggregate_batch_regrid(
    grid_path: str,
    dataset_path: str,
    date_bounds: Annotated[
        list[str], typer.Argument(help="Date min / max pairs to aggregate on")
    ],
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
    out: Annotated[str, typer.Option()] = default_write_path,
):
    # check for the right number of date bounds
    if not (len(date_bounds) % 2 == 0 and len(date_bounds) > 0):
        print(date_bounds)
        print("Provide at least on pair of dates")

    grid = import_grid(grid_path)
    dataset = import_dataset(dataset_path)

    for date_min, date_max in zip(date_bounds[::2], date_bounds[1::2]):
        for variable in ALL_VARIABLES:
            aggregate_data = blur_timerange(dataset, variable, date_min, date_max)
            regridded_aggregate = regrid_data(grid, aggregate_data, (width, height))

            output_path = Path(out) / (
                Path(dataset_path).stem + f"_{variable.value}@{date_min}-{date_max}.nc"
            )
            print("Saving regridded dataset aggregation to", output_path)
            save_dataset_2d(regridded_aggregate, variable, output_path)


@app.command()
def regrid_to_image(
    regridded_data_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.SALINITY_BOTTOM,
    dataset_min: Annotated[float, typer.Option()] = -float("inf"),
    dataset_max: Annotated[float, typer.Option()] = float("inf"),
    out: Annotated[str, typer.Option()] = default_write_path,
):
    dataset = import_regridded_dataset(regridded_data_path, variable)
    width, height = dataset.shape
    computed_min, computed_max = compute_dataset_bounds(dataset)
    image_min = (
        # dataset_min
        computed_min if dataset_min == -float("inf") else dataset_min
    )
    image_max = (
        # dataset_max
        computed_max if dataset_max == float("inf") else dataset_max
    )

    image = create_image(dataset, width, height, variable, image_min, image_max)
    # Use the input path but rename to change the extension .tif
    output_path = Path(out) / (Path(regridded_data_path).stem + ".tif")
    print("Saving regridded image to", output_path)
    save_image(image, output_path)


@app.command()
def regrid_to_images(
    variable: Annotated[OSOMVariables, typer.Argument(help="Variable to regrid")],
    dataset_min: float,
    dataset_max: float,
    dataset_dir: Annotated[str, typer.Argument(help="Datasets to process")],
    out: Annotated[str, typer.Option()] = default_write_path,
):
    for dataset_path in list(Path(dataset_dir).iterdir()):
        output_path = Path(out) / (dataset_path.stem + ".tif")
        if output_path.exists():
            continue
        dataset = import_regridded_dataset(dataset_path, variable)
        width, height = dataset.shape
        image = create_image(dataset, width, height, variable, dataset_min, dataset_max)
        save_image(image, output_path)


@app.command()
def georef_dir(src: str, dst: str):
    if not os.path.exists(dst):
        os.mkdir(dst)
    make_mbtile_for_dir(src, dst)


@app.command()
def make_gif(src_dir: str, out: str):
    save_gif(src_dir, out)


@app.command()
def compute_bounds(
    dataset_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.SALINITY_BOTTOM,
):
    if not os.path.exists(dataset_path_or_dir):
        raise f"Path {dataset_path_or_dir} does not exist"
    if os.path.isfile(dataset_path_or_dir):
        dataset_min, dataset_max = determine_bounds_for_dataset(
            dataset_path,
            variable,  # surface_or_bottom
        )
        print(dataset_min, dataset_max)
    else:
        exit(-1)


@app.command()
def batch_compute_bounds(
    variable: Annotated[OSOMVariables, typer.Argument(help="Variable to regrid")],
    dataset_dir: Annotated[
        str, typer.Argument(help="Directory of datasets to process")
    ],
):
    collection_min, collection_max = determine_bounds_for_collection(
        dataset_dir, variable
    )
    print(collection_min, collection_max)


if __name__ == "__main__":
    app()
