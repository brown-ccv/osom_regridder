#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=32G
#SBATCH -t 4:00:00
#SBATCH -J OsomRegridderMakeImages
#SBATCH --array=0-11

# A script to turn a directory of regridded NetCDFs and files into images.

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

###############################################################################
############################## Run Parameters #################################
###############################################################################

# Variables for Bounds computation / image creation.

VARIABLES=(SurfaceHeight SalinityBottom SalinitySurface WaterTempBottom WaterTempSurface VelocityEastwardBottom VelocityEastwardSurface VelocityNorthwardBottom VelocityNorthwardSurface KineticEnergyBottom KineticEnergySurface)
VARIABLE_INDEX=$SLURM_ARRAY_TASK_ID
VARIABLE=${VARIABLES[$VARIABLE_INDEX]}

function setup_env() {
  source .venv/bin/activate
}

function clean_env() {
  # Exit the python environment
  deactivate
}

function main() {
  setup_env

  echo "$VARIABLE"
  
  python3 -m osom_regridder regrid-to-images --out $OUTPUT_DIR_TMP/$OUTPUT_DIR_IMAGES $VARIABLE -- $(cat bounds-$VARIABLE.txt) $OUTPUT_DIR_TMP/$OUTPUT_DIR_DATA/$VARIABLE

  clean_env
}

main $@
