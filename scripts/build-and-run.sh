#!/bin/bash

rm dist/osom_regridder-*
uv build
uv pip install dist/osom_regridder-*.whl
#python3 -m osom_regridder regrid data/osom_grid.nc data/osom_data_6210.nc --variable temp
#python3 -m osom_regridder display out/osom_data_6210_temp@1.nc temp
#python3 -m osom_regridder map --help
#python3 -m osom_regridder map data/osom_grid.nc
#python3 -m osom_regridder regrid-at-timepoint --help
#python3 -m osom_regridder regrid-at-timepoint data/osom_grid.nc data/osom_data_6210.nc --variable temp
#python3 -m osom_regridder display out/osom_data_6210_temp@1.nc temp
python3 -m osom_regridder regrid --help
python3 -m osom_regridder regrid data/osom_grid.nc data/osom_data_6210.nc --variable temp