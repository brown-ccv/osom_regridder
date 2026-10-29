#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=20G
#SBATCH -t 1:00:00
#SBATCH -J OsomRegridderMakeGif
#SBATCH --array=0-11

# A script to take all the images in a directory and turn them into a single GIF.

module load python/3.11
module load gdal

###############################################################################
################################ Constants ####################################
###############################################################################

RUN_ID="123456"

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
  
  python3 -m osom_regridder make-gif $OUTPUT_DIR_TMP/$OUTPUT_DIR_IMAGES/$VARIABLE $OUTPUT_DIR_TMP/$OUTPUT_DIR_IMAGES/$VARIABLE.gif

  clean_env
}

main $@
