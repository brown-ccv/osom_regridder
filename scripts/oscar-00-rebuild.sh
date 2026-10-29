#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=4G
#SBATCH -t 10:00
#SBATCH -J OsomRegridderBuild

# This script rebuilds the python project and installs it into the current 
# virutal environment. This is used when you're making changes to the Python 
# code and are running array jobs with that changed code. You have to rebuild
# the project first, and then start the array job, otherwise each array job 
# will individually try and rebuild the project and some will fail because of
# race conditions. 

module load python/3.11
module load gdal

function rebuild() {
  rm -rf .venv
  uv venv
  source .venv/bin/activate
  uv sync
  uv build
  uv pip install dist/osom_regridder-*.whl
}

function clean_env() {
  # Exit the python environment
  deactivate
}

function main() {
  rebuild
  
  clean_env
}

main $@
