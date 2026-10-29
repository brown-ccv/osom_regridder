#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=32G
#SBATCH -t 4:00:00
#SBATCH -J OsomRegridderComputeBounds
#SBATCH --array=0-11

# Script to determine dataset bounds for regridded NetCDF files.
# Output files need to be grouped into one folder for each variable.

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
############################## Run Paramters ##################################
###############################################################################

# Variables for Bounds computation / image creation.

VARIABLES=(SurfaceHeight SalinityBottom SalinitySurface WaterTempBottom WaterTempSurface VelocityEastwardBottom VelocityEastwardSurface VelocityNorthwardBottom VelocityNorthwardSurface KineticEnergyBottom KineticEnergySurface)
VARIABLE_INDEX=$SLURM_ARRAY_TASK_ID
VARIABLE=${VARIABLES[$VARIABLE_INDEX]}

function reset() {
  # Create a Python environement and install the package into it.

  rm -rf .venv
  uv venv
  source .venv/bin/activate
  uv sync
  uv build
  uv pip install dist/osom_regridder-*.whl
}

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
  
  python3 -m osom_regridder batch-compute-bounds $VARIABLE $OUTPUT_DIR_TMP/$OUTPUT_DIR_DATA/$VARIABLE > bounds-$VARIABLE.txt

  # Remove the data file
  rm $OUTPUT_DIR_TMP/$DATA_FILE

  clean_env
}

main $@
