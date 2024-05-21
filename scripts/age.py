import csv

additional_input_file = (
    "data/census-data/UV101b - Usual resident population by sex by age (6).csv"
)
output_file = "output/census_ages.csv"

# Process the additional input file and write the output
with open(additional_input_file, "r") as file, open(
    output_file, "w", newline=""
) as output:
    reader = csv.reader(file)
    writer = csv.writer(output)
    writer.writerow(
        [
            "Census Tract",
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
            age_group_data = [0 if x == "-" else int(x) for x in row[1:8]]
            writer.writerow([census_tract] + age_group_data)
