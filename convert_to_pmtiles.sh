#!/bin/bash

# Directories containing GeoJSON files
directories=("output/output-areas" "output/intersected")

# Loop through each directory
for dir in "${directories[@]}"; do
    # Loop through each GeoJSON file in the directory
    for file in "$dir"/*.geojson; do
        echo "Starting conversion of $file at $(date)"
        
        # Define the output pmtiles file path
        output_file="output/pmtiles/${file##*/}"
        output_file="${output_file%.geojson}.pmtiles"
        
        # Set common Tippecanoe options
        common_options=(
            --output="$output_file"
            --layer="maplayer"
            --detect-shared-borders
            --coalesce-fraction-as-needed
            --coalesce-densest-as-needed
            --coalesce-smallest-as-needed
            --increase-gamma-as-needed
            --coalesce
            --reorder
            --minimum-zoom=0
            --maximum-zoom=17
            --force
            --simplification=20
        )
        
        # Add directory-specific options
        if [[ "$dir" == "output/output-areas" ]]; then
            tippecanoe "${common_options[@]}" --no-feature-limit --no-tile-size-limit "$file"
        elif [[ "$dir" == "output/intersected" ]]; then
            tippecanoe "${common_options[@]}" --no-feature-limit "$file"
        fi
        
        echo "Finished conversion of $file at $(date)"
    done
done

echo "Conversion to PMTiles completed."