#!/bin/bash
#SBATCH -n 1
#SBATCH --mem=8G
#SBATCH -t 1:30:00
#SBATCH -J OsomRegridder

OUTPUT_HEIGHT=1600
OUTPUT_WIDTH=2600
GRID_PATH='/oscar/data/epscor/OSOM/input/ROMS_forcing_files/grid/osom_grid4_mindep_smlp_mod10.nc'

function setup_env() {
  # Load Oscar Modules

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

function regrid_at_timepoint() {
  # Regrid a file at a given timepoint for a specific variable.
  # Will write to a new .nc file in out/ as per osom_regridder.
  local file_path="${1}"
  local variable="${2}"
  local timepoint="${3:-8}"
  
  echo "Regridding ${file_path}..."
  python3 -m osom_regridder regrid-at-timepoint \
    "${GRID_PATH}" "${file_path}" \
    --variable "${variable}" \
    --height "${OUTPUT_HEIGHT}" \
    --width "${OUTPUT_WIDTH}" \
    --timepoint "${timepoint}"
}

function find_min_max_for_variable() {
  # Implementation of the Champion algorithm for determining
  # min and max of a variable for a given dataset.
  local variable="${1}"
  # Arbitrarily large / small values. 
  local min=10000.0
  local max=-10000.0

  while IFS= read -r file_path; do
    [ -f "${file_path}" ] || continue
    file_min_and_max="$(python3 -m osom_regridder compute-dataset-bounds "${file_path}" --variable "${variable}")"

    file_min="$(echo "${file_min_and_max}" | awk '{print $1}')"
    file_max="$(echo "${file_min_and_max}" | awk '{print $2}')"

   echo "${file_min_max} ${min} ${max}"

    if [ "$(echo "${file_min} < ${min}" | bc)" -eq 1 ]; then
      temp_min=${file_min}
    fi
    if [ "$(echo "${file_max} > ${max}" | bc)" -eq 1 ]; then
      temp_max=${file_max}
    fi  
  done < yearly_regrid.txt

  echo "${min} ${max}"
}

function create_image() {
  # Creates a TIFF image based on regridded NC data and computed bounds.
  local variable="${1}"
  local min="${2}"
  local max="${3}"
  local regrid_glob="${4}"

  for regridded_file in $regrid_glob; do
    python3 -m osom_regridder regrid-to-image "${regridded_file}" \
      --variable "${variable}" \
      --dataset-min "{$min}" \
      --dataset-max "${max}"
  done
}

function main() {
  setup_env

  # Regrid all files

  while IFS= read -r file_path; do
    [ -f "${file_path}" ] || continue
    #regrid_at_timepoint "${file_path}" 'temp'
    #regrid_at_timepoint "${file_path}" 'salt'
    #regrid_at_timepoint "${file_path}" 'AKv'
  done < yearly_regrid.txt

  # Determine bounds for each variable.

  #temp_min_and_max=$(find_min_max_for_variable 'temp')
  #temp_min="$(echo "${temp_min_and_max}" | awk '{print $1}')"
  #temp_max="$(echo "${temp_min_and_max}" | awk '{print $2}')"

  #salt_min_and_max=$(find_min_max_for_variable 'salt')
  #salt_min="$(echo "${salt_min_and_max}" | awk '{print $1}')"
  #salt_max="$(echo "${salt_min_and_max}" | awk '{print $2}')"

  akv_min_and_max=$(find_min_max_for_variable 'AKv')
  akv_min="$(echo "${akv_min_and_max}" | awk '{print $1}')"
  akv_max="$(echo "${akv_min_and_max}" | awk '{print $2}')"

  echo "Temp Bounds: $temp_min - $temp_max
  Salt Bounds: $salt_min - $salt_max
  AKv Bounds: $akv_min - $akv_max" > bounds.txt

  # Create images based on bounds and regridded NC files

  #create_image 'temp' "${temp_min}" "${temp_max}" 'out/*_temp@8.nc'
  #create_image 'salt' "${salt_min}" "${salt_max}" 'out/*_salt@8.nc'
  create_image 'AKv' "${akv_min}" "${akv_max}" 'out/*_AKv@8.nc'

  # Tile TIFF images into .mbtiles files in tiles/

  python3 -m osom_regridder georef-dir out tiles

  clean_env
}

main $@
