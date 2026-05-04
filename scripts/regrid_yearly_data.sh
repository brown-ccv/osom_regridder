#!/bin/bash
#SBATCH -n 1
#SBATCH --mem=8G
#SBATCH -t 1:30:00
#SBATCH -J OsomRegridder

output_height=1600
output_width=2600
grid_path="/oscar/data/epscor/OSOM/input/ROMS_forcing_files/grid/osom_grid4_mindep_smlp_mod10.nc"

# Setup Environment 

module load gdal

rm -rf .venv
uv venv
source .venv/bin/activate
uv sync
uv build
uv pip install dist/osom_regridder-*.whl

# Regrid Datasets

files=$(cat yearly_regrid.txt)

for file_path in $files
do
  [ -f "$file_path" ] || continue
  echo "Regridding $file_path..."
  python3 -m osom_regridder regrid-at-timepoint "$grid_path" "$file_path" --variable temp --height "$output_height" --width "$output_width" --timepoint 8
  python3 -m osom_regridder regrid-at-timepoint "$grid_path" "$file_path" --variable salt --height "$output_height" --width "$output_width" --timepoint 8
  python3 -m osom_regridder regrid-at-timepoint "$grid_path" "$file_path" --variable AKv --height "$output_height" --width "$output_width" --timepoint 8
done

# Compute Dataset Range

temp_min=100
temp_max=0

salt_min=100
salt_max=0

akv_min=100
akv_max=0

for file_path in $files
do
  [ -f "$file_path" ] || continue
  min_and_max_temp=$(python3 -m osom_regridder compute-dataset-bounds "$file_path" --variable temp)
  min_and_max_salt=$(python3 -m osom_regridder compute-dataset-bounds "$file_path" --variable salt)
  min_and_max_akv=$(python3 -m osom_regridder compute-dataset-bounds "$file_path" --variable AKv)

  # Temp Championing

  min_and_max_temp_array=($min_and_max_temp)
  if (( $(echo "${min_and_max_temp_array[0]} $temp_min" | awk '{print ($1 < $2)}') )); then
    temp_min=${min_and_max_temp_array[0]}
  fi
  if (( $(echo "${min_and_max_temp_array[1]} $temp_min" | awk '{print ($1 > $2)}') )); then
    temp_max=${min_and_max_temp_array[1]}
  fi  

  # Salt Championing
  
  min_and_max_salt_array=($min_and_max_salt)
  if (( $(echo "${min_and_max_salt_array[0]} $salt_min" | awk '{print ($1 < $2)}') )); then
    salt_min=${min_and_max_salt_array[0]}
  fi
  if (( $(echo "${min_and_max_salt_array[1]} $salt_min" | awk '{print ($1 > $2)}') )); then
    salt_max=${min_and_max_salt_array[1]}
  fi

  # Kinetic Energy templating

  min_and_max_akv_array=($min_and_max_akv)
  if (( $(echo "${min_and_max_akv_array[0]} $akv_min" | awk '{print ($1 < $2)}') )); then
    akv_min=${min_and_max_akv_array[0]}
  fi
  if (( $(echo "${min_and_max_akv_array[1]} $akv_min" | awk '{print ($1 > $2)}') )); then
    akv_max=${min_and_max_akv_array[1]}
  fi  
done

echo "Temp Bounds: $temp_min - $temp_max
Salt Bounds: $salt_min - $salt_max
AKv Bounds: $akv_min - $akv_max" > bounds.txt

# Create Images

for regridded_file in out/*_temp@8.nc;
do
  python3 -m osom_regridder regrid-to-image "$regridded_file" --variable temp --dataset-min "$temp_min" --dataset-max "$temp_max"
done


for regridded_file in out/*_salt@8.nc;
do
  python3 -m osom_regridder regrid-to-image "$regridded_file" --variable salt --dataset-min "$temp_min" --dataset-max "$temp_max"
done

for regridded_file in out/*_AKv@8.nc;
do
  python3 -m osom_regridder regrid-to-image "$regridded_file" --variable AKv --dataset-min "$akv_min" --dataset-max "$akv_max"
done

# Georeference Images

python3 -m osom_regridder georef-dir out tiles

# Cleanup

deactivate
