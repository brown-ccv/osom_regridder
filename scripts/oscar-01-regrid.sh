#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=100G
#SBATCH -t 1-00:00:00
#SBATCH -J OsomRegridderRegridTiles
#SBATCH --array=2005-2022

# SBATCH Array for each day for Irene Run: --array=27-30
# SBATCH Array for each year: --array=2005-2022

# Script to regrid data files into new NetCDF files.

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

DATA_FILE="${YEAR}_surf_his.nc"

MONTHLY_RANGES="${YEAR}-01-01T00:00 ${YEAR}-01-31T00:00 ${YEAR}-02-01T00:00 ${YEAR}-02-28T00:00 ${YEAR}-03-01T00:00 ${YEAR}-03-31T00:00 ${YEAR}-04-01T00:00 ${YEAR}-04-30T00:00 ${YEAR}-05-01T00:00 ${YEAR}-05-31T00:00 ${YEAR}-06-01T00:00 ${YEAR}-06-30T00:00 ${YEAR}-07-01T00:00 ${YEAR}-07-31T00:00 ${YEAR}-08-01T00:00 ${YEAR}-08-31T00:00 ${YEAR}-09-01T00:00 ${YEAR}-09-30T00:00 ${YEAR}-10-01T00:00 ${YEAR}-10-31T00:00 ${YEAR}-11-01T00:00 ${YEAR}-11-30T00:00 ${YEAR}-12-01T00:00 ${YEAR}-12-31T00:00"
IRENE_TIMEPOINTS="${DATE}T00:00 ${DATE}T01:30 ${DATE}T03:00 ${DATE}T04:30 ${DATE}T06:00 ${DATE}T07:30 ${DATE}T09:00 ${DATE}T10:30 ${DATE}T12:00 ${DATE}T13:30 ${DATE}T15:00 ${DATE}T16:30 ${DATE}T18:00 ${DATE}T19:30 ${DATE}T21:00 ${DATE}T22:30"

TIMEPOINTS=$IRENE_TIMEPOINTS

# Year for Full Model Run

# YEAR=$SLURM_ARRAY_TASK_ID

# Date composition for Irene Model Run:

YEAR="2011"
MONTH="08"
DAY=$SLURM_ARRAY_TASK_ID
DATE="${YEAR}-${MONTH}-${DAY}"

function setup_env() {
  source .venv/bin/activate
}

function clean_env() {
  # Exit the python environment
  deactivate
}

function main() {
  setup_env

  echo "$DATE"
  # Copy the data file to jobtmp
  cp $DATA_DIR/$DATA_FILE $OUTPUT_DIR_TMP/$DATA_FILE
  
  # Genereate the regridded data files
  python3 -m osom_regridder batch-regrid $GRID_PATH $DATA_DIR/$DATA_FILE $TIMEPOINTS --out $OUTPUT_DIR_TMP/$OUTPUT_DIR_DATA
  
  # Batch Regrid Command
  # python3 -m osom_regridder aggregate-batch-regrid $GRID_PATH $DATA_DIR/$DATA_FILE $TIMEPOINTS --out $OUTPUT_DIR_TMP/$OUTPUT_DIR_DATA
  
  # Remove the data file
  rm $OUTPUT_DIR_TMP/$DATA_FILE

  clean_env
}

main $@
