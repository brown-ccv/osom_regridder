#!/bin/bash

gdal_translate out/osom_data_6210_temp@1.tif out/6210_temp.tif -of GTiff -a_srs EPSG:4326 -a_ullr -72.7 41.9 -69.96 40.5
gdal_translate out/6210_temp.tif out/6210_temp.mbtiles -of MBTILES
gdaladdo -r average out/6210_temp.mbtiles 2 4 8 16 32 64 128 256

