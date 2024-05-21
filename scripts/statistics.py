from dictionary import csv_files
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
        total_column = {
            "ages": "Total",
            "ethnic-group": "All People",
            "national-identity": "All people",
            "multiple-ethnic-groups": "All occupied households",
            "nationalities": "All people",
            "religion": "All people",
            "passports-held": "All people",
            "gaelic-language-skills": "All people aged 3 and over",
            "scots-language-skills": "All people aged 3 and over",
            "english-language-skills": "All people aged 3 and over",
            "bsl-skills": "All people aged 3 and over",
            "main-language": "All people aged 3 and over",
            "household-size": "All occupied household spaces",
        }[description]

        # Calculate percentages for each column
        for column in df.columns:
            if column != total_column:
                df[column] = df[column] / df[total_column] * 100

        # Calculate and store statistics for each column
        file_results = {}
        for column in df.columns:
            if column != total_column:
                mean = df[column].mean()
                std_dev = df[column].std()
                mean_minus_std = max(mean - std_dev, 0)
                mean_plus_std = mean + std_dev

                file_results[column] = {
                    "mean": round(mean, 2),
                    "low": round(mean_minus_std, 2),
                    "high": round(mean_plus_std, 2),
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
