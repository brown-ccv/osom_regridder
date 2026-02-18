#!/bin/bash

# Note (AM): This was written by AI because my GDAL Python bindings were broken. 
# Given an input and an output directory, this will convert all tif files into 
# georeferenced MBTILES files that can be served by a tile server.

# Check if two arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <input_dir> <output_dir>"
    exit 1
fi

input_dir="$1"
output_dir="$2"

# Validate input directory
if [ ! -d "$input_dir" ]; then
    echo "Error: Input directory does not exist: $input_dir"
    exit 1
fi

# Ensure output directory exists
mkdir -p "$output_dir"

# Process each .tif file in the input directory
for file in "$input_dir"/*.tif; do
    if [ -f "$file" ]; then
        # Extract base name without extension
        base_name="${file##*/}"
        base_name="${base_name%.tif}"
        output_file="$output_dir/$base_name.mbtiles"
        echo "$file $output_file"
        # Run gdal_translate
        gdal_translate "$file" "$output_file" -of MBTILES \
            -a_srs EPSG:4326 -a_ullr -72.7 41.9 -69.96 40.5

        # Check if the MBTILES file was created
        if [ -f "$output_file" ]; then
            # Run gdaladdo to add overviews
            gdaladdo -r average "$output_file" 2 4 8 16 32 64 128
        else
            echo "Failed to generate MBTILES file for: $file"
        fi
    fi
done

echo "Processing completed."
