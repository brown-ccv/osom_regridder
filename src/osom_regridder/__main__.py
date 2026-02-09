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
from .regrid import regrid_timepoint, regrid_dataset

from .output import create_image, save_image, save_dataset_2d, save_dataset_3d

app = typer.Typer(no_args_is_help=True)


default_height = 160
default_width = 260


class OSOMVariables(str, Enum):
    TEMP = "temp"
    SALT = "salt"
    ZETA = "zeta"
    UBAR_EAST = "ubar_eastward"
    UBAR_WEST = "ubar_westward"


class SurfaceOrBottom(str, Enum):
    SURFACE = "surface"
    BOTTOM = "bottom"


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
    # Use the input path but rename to change the extension .tif
    output_path = Path("out/") / (Path(regridded_data_path).stem + ".tif")
    print("Saving regridded image to", output_path)
    save_image(image, output_path)


if __name__ == "__main__":
    app()
