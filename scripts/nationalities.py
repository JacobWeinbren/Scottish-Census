import csv

# Path to the input CSV file
input_file_path = (
    "data/census-data/UV204b - Country of birth (14) by sex by age (6).csv"
)

# Path to the output file
output_file_path = "output/census_nationalities.csv"

# Open the input CSV file
with open(input_file_path, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)

    for _ in range(4):
        next(reader)

    # Read the header rows
    nationality_header = next(reader)
    gender_header = next(reader)
    age_header = next(reader)

    # Find indices where gender is 'All people' and age is 'Total'
    indices = [
        index
        for index, (gender, age) in enumerate(zip(gender_header, age_header))
        if gender == "All people" and age == "Total"
    ]

    # Prepare to write to the output file
    with open(output_file_path, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.writer(outfile)

        # Write the header row: Tract and nationalities
        writer.writerow(["Tract"] + [nationality_header[i] for i in indices])

        # Read each data row and extract values for the filtered indices
        for row in reader:
            if len(row) > max(indices):  # Ensure the row has all required columns
                tract = row[0]
                if tract:  # Check if the tract identifier is valid (non-empty)
                    values = [row[i] for i in indices]
                    writer.writerow([tract] + values)

print(f"Total values for all people by tract saved to {output_file_path}")
