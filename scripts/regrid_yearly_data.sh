#!/bin/bash
#SBATCH -n 4
#SBATCH --mem=32G
#SBATCH -t 4:00:00
#SBATCH -J JOBNAME

output_height=1600
output_width=2600
grid_path="/oscar/data/epscor/OSOM/input/ROMS_forcing_files/grid/osom_grid4_mindep_smlp_mod10.nc"

# Setup Environment 

rm -rf .venv
uv venv
source .venv/bin/activate
uv sync
uv build
uv pip install dist/osom_regridder-*.whl

# Regrid Datasets

files=$(./scripts/osom-regridder-paths range 2005/01/01 2022/01/01 year)

for file_path in $files
do
  [ -f "$file_path" ] || continue
  echo "Regridding $file_path..."
  python3 -m osom_regridder regrid-at-timepoint "$grid_path" "$file_path" --variable temp --height "$output_height" --width "$output_width"
  python3 -m osom_regridder regrid-at-timepoint "$grid_path" "$file_path" --variable salt --height "$output_height" --width "$output_width"
done

# Compute Dataset Range

temp_min=100
temp_max=0

for regridded_file in out/*_temp@1.nc;
do
  min_and_max=$(python3 -m osom_regridder compute-dataset-bounds "$regridded_file" --variable temp)
  min_and_max_array=($min_and_max)
  if [ ${min_and_max_array[0]} -lt $temp_min ]; then
    temp_min=${min_and_max_array[0]}
  fi
  if [ ${min_and_max_array[1]} -gt $temp_max ]; then
    temp_max=${min_and_max_array[1]}
  fi
done

salt_min=100
salt_max=0

for regridded_file in out/*_salt@1.nc;
do
  min_and_max=$(python3 -m osom_regridder compute-dataset-bounds "$regridded_file" --variable salt)
  min_and_max_array=($min_and_max)
  if [ ${min_and_max_array[0]} -lt $salt_min ]; then
    salt_min=${min_and_max_array[0]}
  fi
  if [ ${min_and_max_array[1]} -gt $salt_max ]; then
    salt_max=${min_and_max_array[1]}
  fi
done

# Create Images

for regridded_file in out/*_temp@1.nc;
do
  python3 -m osom_regridder regrid_to_image "$regridded_file" --variable temp --dataset-min "$temp_min" --dataset-max "$temp_max"
done


for regridded_file in out/*_salt@1.nc;
do
  python3 -m osom_regridder regrid_to_image "$regridded_file" --variable salt --dataset-min "$temp_min" --dataset-max "$temp_max"
done

# Georeference Images

python3 -m osom_regridder georef-dir out tiles

# Cleanup

deactivate
