#!/bin/bash

module load gdal

rm -rf .venv
uv venv
source .venv/bin/activate
uv sync
uv build
uv pip install dist/osom_regridder-*.whl

python3 -m osom_regridder compute-dataset-bounds /oscar/data/epscor/OSOM/output/OSOM_v2/2005/ocean_his_0001.nc --variable salt

#python3 -m osom_regridder compute-dataset-bounds out/ocean_his_1096_salt@1.nc --variable salt
