#!/bin/bash

uv build
uv pip install dist/osom_regridder-0.1.0-py3-none-any.whl
python3 -m osom_regridder regrid data/osom_grid.nc data/osom_data_6210.nc --variable temp
python3 -m osom_regridder display out/osom_data_6210_temp@1.nc temp
