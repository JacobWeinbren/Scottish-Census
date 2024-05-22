from dictionary import csv_files, total_column
import pandas as pd
import numpy as np
import json
import os


def calculate_statistics(file_path, description, skip_rows):
    results = {}
    try:
        # Load the CSV file into a DataFrame, skipping initial rows and setting the first column as index
        df = pd.read_csv(file_path, skiprows=skip_rows, index_col=0)

        # Filter rows where the index starts with 'S'
        df = df[df.index.str.startswith("S")]

        # Replace '-' with 0 and convert all columns to numeric, errors='coerce' will convert non-convertible values to NaN
        df = df.replace("-", 0).apply(pd.to_numeric, errors="coerce")
        # Get the total column based on the description
        total_column_name = total_column[description]

        # Calculate percentages for each column
        for column in df.columns:
            if column != total_column_name:
                df[column] = df[column] / df[total_column_name] * 100

        # Calculate and store statistics for each column
        file_results = {}
        for column in df.columns:
            if column != total_column_name:
                median = df[column].median()
                q1 = df[column].quantile(0.02)
                q3 = df[column].quantile(0.98)

                file_results[column] = {
                    "median": round(median, 2),
                    "low": round(q1, 2),
                    "high": round(q3, 2),
                }

        results[description] = file_results

    except Exception as e:
        print(f"Failed to process {file_path}: {str(e)}")

    return results


# Dictionary to hold all results
all_results = {}

# Loop through each file in csv_files and calculate statistics
for file_path, skip_rows, description in csv_files:
    file_results = calculate_statistics(file_path, description, skip_rows)
    all_results.update(file_results)

# Save all results to a single JSON file
output_path = os.path.join("output", "all_statistics.json")
with open(output_path, "w") as json_file:
    json.dump(all_results, json_file, indent=4)
    print(f"All results saved to {output_path}")
