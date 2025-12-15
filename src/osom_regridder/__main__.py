"""
The command line interface for the OSOM regridding tool.

Commands:
 - regrid: takes a file (and optional a grid dims), and runs the regrid process.
 - display: takes a regridded image and creates a basic image visualization for it.
 - tile: takes raw OSOM data and regrids it, and then formats it info a servable mbtiles file.
   - option to perform this at 1 time point or ALL time points.

"""

import typer
from enum import Enum
from typing_extensions import Annotated
from .file_input import import_grid, import_dataset, import_regridded_dataset
from .regrid import populate_regrid
from .output import create_image, save_image, save_dataset

app = typer.Typer(no_args_is_help=True)


default_height = 16
default_width = 26


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
def regrid(
    grid_path: str,
    dataset_path: str,
    variable: Annotated[OSOMVariables, typer.Option()] = OSOMVariables.TEMP.value,
    surfaceOrBottom: Annotated[
        SurfaceOrBottom, typer.Option()
    ] = SurfaceOrBottom.SURFACE.value,
    timepoint: Annotated[int, typer.Option(help="Days since model inception.")] = 1,
    height: Annotated[int, typer.Option()] = default_height,
    width: Annotated[int, typer.Option()] = default_width,
):
    lat, lon, mask, bathymetry = import_grid(grid_path)
    data = import_dataset(dataset_path, variable, surfaceOrBottom)
    data_at_timepoint = data[timepoint]
    regridded = populate_regrid(width, height, lon, lat, data_at_timepoint)
    # Use the input path but add variable and timepoint ID.
    output_path = (
        "out/"
        + ".".join(dataset_path.split("/")[-1].split(".")[:-1])
        + f"_{variable.value}@{timepoint}.nc"
    )
    print("Saving regridded dataset to", output_path)
    save_dataset(regridded, variable, output_path)


@app.command()
def tile():
    raise "Not Implemented."


@app.command()
def display(regridded_data_path: str, variable: str):
    dataset = import_regridded_dataset(regridded_data_path, variable)
    width, height = dataset.shape
    image = create_image(dataset, width, height)
    # Use the input path but rename to change the extension .png
    output_path = (
        "out/" + ".".join(regridded_data_path.split("/")[-1].split(".")[:-1]) + ".png"
    )
    save_image(image, output_path)


if __name__ == "__main__":
    app()
