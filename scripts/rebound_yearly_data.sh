#!/bin/bash
#SBATCH -n 1
#SBATCH --mem=8G
#SBATCH -t 1:30:00
#SBATCH -J OsomRegridder-Rebound

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

temp_min=-6.68
temp_max=27.39

salt_min=0
salt_max=33.07

# Create Images

for regridded_file in out/*_temp@8.nc;
do
  python3 -m osom_regridder regrid-to-image "$regridded_file" --variable temp --dataset-min "$temp_min" --dataset-max "$temp_max"
done


for regridded_file in out/*_salt@8.nc;
do
  python3 -m osom_regridder regrid-to-image "$regridded_file" --variable salt --dataset-min "$temp_min" --dataset-max "$temp_max"
done

# Georeference Images

python3 -m osom_regridder georef-dir out tiles

# Cleanup

deactivate
