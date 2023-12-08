#!/bin/bash
# Authors: Jean Martial Mari & Chat GPT
# This script processes LiDAR data and outputs it in x;y;z;intensity format.

# Function to process a line of LiDAR data
process_lidar_data() {
    while read -r line; do
        if [[ $line =~ angle:([0-9]+\.[0-9]+),distance\(mm\):([0-9]+),intensity:([0-9]+) ]]; then
            angle=${BASH_REMATCH[1]}
            distance=${BASH_REMATCH[2]}
            intensity=${BASH_REMATCH[3]}

            # Convert polar coordinates to Cartesian coordinates (assuming z=0)
            rad=$(echo "$angle * 3.14159265 / 180" | bc -l)
            x=$(echo "$distance * c($rad)" | bc -l)
            y=$(echo "$distance * s($rad)" | bc -l)
            z=0

            echo "$x;$y;$z;$intensity"
        fi
    done
}

# Check if a filename is provided
if [ -z "$1" ]; then
    # No filename provided, output to stdout
    ./saveLidar2File.sh | process_lidar_data
else
    # Filename provided, output to file
    ./saveLidar2File.sh | process_lidar_data > "$1"
fi
