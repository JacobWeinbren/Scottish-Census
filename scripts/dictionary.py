import csv
import string


def generate_key(index):
    if index < 26:
        return string.ascii_lowercase[index]
    else:
        return generate_key(index // 26 - 1) + string.ascii_lowercase[index % 26]


def create_key_mapping(csv_files):
    key_mapping = {}
    current_index = 0

    for file_path, skip_rows, _ in csv_files:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            for _ in range(skip_rows):
                next(reader)
            header = next(reader)
            for key in header:
                if key not in key_mapping:
                    key_mapping[key] = generate_key(current_index)
                    current_index += 1

    return key_mapping