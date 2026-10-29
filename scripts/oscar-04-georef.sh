#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=32G
#SBATCH -t 16:00:00
#SBATCH -J OsomRegridderGeoref

# A script to georeference a directory of images and create mbtiles.

module load python/3.11
module load gdal

RUN_ID="123456"

###############################################################################
################################ Constants ####################################
###############################################################################

GRID_PATH='/oscar/data/epscor/OSOM/input/ROMS_forcing_files/grid/osom_grid4_mindep_smlp_mod10.nc'
DATA_DIR='/oscar/data/epscor/bke/erddap/data/netcdf/osom_v2'
OUTPUT_DIR_TMP="/jobtmp/amurph40/osom_regridder/$RUN_ID"

OUTPUT_DIR_DATA='data'
OUTPUT_DIR_IMAGES='images'
OUTPUT_DIR_TILES='tiles'

function setup_env() {
  source .venv/bin/activate
}

function clean_env() {
  # Exit the python environment
  deactivate
}

function main() {
  setup_env

  python3 -m osom_regridder georef-dir $OUTPUT_DIR_TMP/$OUTPUT_DIR_IMAGES $OUTPUT_DIR_TMP/$OUTPUT_DIR_TILES
  
  clean_env
}

main $@
