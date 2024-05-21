import csv
import numpy as np
import wquantiles


def calculate_weighted_median_age(ages, weights):
    if not ages or not weights:
        return None
    # Convert lists to numpy arrays
    ages_array = np.array(ages)
    weights_array = np.array(weights)
    return round(wquantiles.median(ages_array, weights=weights_array), 1)


input_file = "data/census-data/UV103 - Age by single year.csv"
additional_input_file = (
    "data/census-data/UV101b - Usual resident population by sex by age (6).csv"
)
output_file = "output/census_ages.csv"

# Dictionary to store median ages for each census tract
tract_median_ages = {}

# Process the first input file to calculate median weighted age for each census tract
with open(input_file, "r") as file:
    reader = csv.reader(file)
    for _ in range(3):  # Skip the first 3 rows
        next(reader)
    age_categories = next(reader)  # This should now be the row with age categories

    for row in reader:
        if len(row) and row[0].startswith(
            "S"
        ):  # Check if the row is likely to be valid data
            census_tract = row[0]
            ages = []
            weights = []
            for age_index, count in enumerate(row[2:], start=2):
                if count.isdigit():
                    age_label = age_categories[age_index]
                    if age_label == "Under 1":
                        age_int = 0
                    elif age_label == "100 and over":
                        age_int = 100
                    else:
                        age_int = int(age_label)
                    weights.append(int(count))
                    ages.append(age_int)
            median_age = calculate_weighted_median_age(ages, weights)
            tract_median_ages[census_tract] = median_age

# Process the additional input file and write the output
with open(additional_input_file, "r") as file, open(
    output_file, "w", newline=""
) as output:
    reader = csv.reader(file)
    writer = csv.writer(output)
    writer.writerow(
        [
            "Census Tract",
            "Median Weighted Age",
            "Total",
            "0 - 15",
            "16 - 24",
            "25 - 34",
            "35 - 49",
            "50 - 64",
            "65 and over",
        ]
    )
    for _ in range(7):  # Skip 4 rows plus 3 header rows
        next(reader)
    for row in reader:
        if len(row) and row[0].startswith(
            "S"
        ):  # Check if the row is likely to be valid data
            census_tract = row[0]
            median_age = tract_median_ages.get(census_tract, "Data Not Available")
            age_group_data = [0 if x == "-" else int(x) for x in row[1:8]]
            writer.writerow([census_tract, median_age] + age_group_data)
