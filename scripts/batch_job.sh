#!/bin/bash
#SBATCH -n 4
#SBATCH --mem=32G
#SBATCH -t 4:00:00
#SBATCH -J JOBNAME

module load python/3.11
python -m pip install uv
python -m uv venv 
source .venv/bin/activate
python -m pip install uv
python -m uv sync
python -m uv build
python -m uv pip install dist/osom_regridder-*.whl
python -m osom_regridder regrid /oscar/data/epscor/OSOM/input/ROMS_forcing_files/grid/osom_grid4_mindep_smlp_mod10.nc /oscar/data/epscor/OSOM/output/OSOM_v2/2022/ocean_his_6210.nc --variable temp