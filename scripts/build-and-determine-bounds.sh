#!/bin/bash

rm dist/osom_regridder-*
uv build
uv pip install dist/osom_regridder-*.whl

python3 -m osom_regridder compute-dataset-bounds data/osom_data_6210.nc --variable temp
