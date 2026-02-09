#!/bin/bash

gdal_translate out/edited_osom_temp.png / -of GTiff -a_srs EPSG:4326 -a_ullr -72.7 41.9 -69.96 40.5
gdal_translate out/edited_osom_temp_georef.tif out/edited_osom_temp.mbtiles -of MBTILES
gdaladdo -r average out/edited_osom_temp.mbtiles 2 4 8 16 32 64 128

 #-71.0726843371978 42.17423565201304 -72.66539077917145 40.92709332092678

#LON_W = -72.7
#LON_E = -69.96
#LAT_N = 41.9
#LAT_S = 40.5

