#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=100G
#SBATCH -t 0:15:00
#SBATCH -J OsomRegridderTest

OUTPUT_HEIGHT=1600
OUTPUT_WIDTH=2600
GRID_PATH='/oscar/data/epscor/OSOM/input/ROMS_forcing_files/grid/osom_grid4_mindep_smlp_mod10.nc'
DATA_PATH='/oscar/data/epscor/bke/erddap/data/netcdf/osom_v2/2005_surf_his.nc'

ALL_VARIABLES='SalinityBottom,SalinitySurface,WaterTempBottom,WaterTempSurface,SurfaceHeight,VelocityEastwardBottom,VelocityEastwardSurface,VelocityNorthwardBottom,VelocityNorthwardSurface,KineticEnergyBottom,KineticEnergySurface'

function setup_env() {
  # Load Oscar Modules

  module load python/3.11
  module load gdal

  # Create a Python environement and install the package into it.

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
  setup_env

  #python3 -m osom_regridder test /oscar/data/epscor/bke/erddap/data/netcdf/osom_v2/2005_surf_his.nc
  
  python3 -m osom_regridder batch-regrid "${GRID_PATH}" "${DATA_PATH}" "${ALL_VARIABLES}" 2005-01-01T12:00,2005-02-01T12:00

  clean_env
}

main $@
