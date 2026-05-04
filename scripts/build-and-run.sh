#!/bin/bash

rm dist/osom_regridder-*
uv build
uv pip install dist/osom_regridder-*.whl
osom_regridder --help
#python3 -m osom_regridder regrid data/osom_grid.nc data/osom_data_6210.nc --variable temp
#python3 -m osom_regridder display out/osom_data_6210_temp@1.nc temp
#python3 -m osom_regridder map --help
#python3 -m osom_regridder map data/osom_grid.nc
#python3 -m osom_regridder regrid-at-timepoint --help
#python3 -m osom_regridder regrid-at-timepoint data/osom_grid.nc data/osom_data_6210.nc --variable temp
#python3 -m osom_regridder display out/osom_data_6210_temp@1.nc temp

# Regrid and Display at 1 Timepoint

#python3 -m osom_regridder regrid-at-timepoint --help
#python3 -m osom_regridder regrid-at-timepoint data/osom_grid.nc data/osom_data_6210.nc --variable temp
#python3 -m osom_regridder display out/osom_data_6210_temp@1.nc temp

# Regrid Dataset at all timepoints and create images

#python3 -m osom_regridder regrid data/osom_grid.nc data/osom_data_6210.nc --variable temp
#python3 -m osom_regridder regrid-to-image --help
#python3 -m osom_regridder regrid-to-images out/osom_data_6210_temp.nc 3.064768 12.107366 --variable temp
#python3 -m osom_regridder regrid-to-images out/osom_data_6210_temp@1.nc temp


# Georef dir

#python3 -m osom_regridder georef-dir out out/osom_6210_temp_tiles
