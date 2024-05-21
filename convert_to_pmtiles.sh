#!/bin/bash

# Directories containing GeoJSON files
directories=("output/intersected" "output/output-areas")

# Loop through each directory
for dir in "${directories[@]}"; do
    # Loop through each GeoJSON file in the directory
    for file in "$dir"/*.geojson; do
        echo "Starting conversion of $file at $(date)"
        
        # Define the output pmtiles file path
        output_file="output/pmtiles/${file##*/}"
        output_file="${output_file%.geojson}.pmtiles"
        
        # Run Tippecanoe to convert GeoJSON to PMTiles
        tippecanoe --output="$output_file" \
                   --layer="maplayer" \
                   --no-feature-limit \
                   --no-tile-size-limit \
                   --detect-shared-borders \
                   --coalesce-fraction-as-needed \
                   --coalesce-densest-as-needed \
                   --coalesce-smallest-as-needed \
                   --coalesce \
                   --reorder \
                   --minimum-zoom=0 \
                   --maximum-zoom=17 \
                   --drop-densest-as-needed \
                   --force \
                   "$file"
        
        echo "Finished conversion of $file at $(date)"
    done
done

echo "Conversion to PMTiles completed."