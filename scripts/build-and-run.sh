#!/bin/bash

uv build
uv pip install dist/osom_regridder-0.1.0-py3-none-any.whl
python3 -m osom_regridder
