import os
import csv
import ujson
import copy
from dictionary import create_key_mapping, csv_files


def load_geojson(path):
    print(f"Loading GeoJSON file from {path}")
    with open(path, "r") as file:
        data = ujson.load(file)
    return data


def save_geojson(data, path):
    print(f"Saving GeoJSON data to {path}")
    with open(path, "w") as file:
        ujson.dump(data, file, indent=1)
    print(f"Data saved successfully to {path}")


def update_feature(feature, code_key, properties):
    if feature["properties"].get(code_key) == properties["code"]:
        feature["properties"].update(
            {k: properties[k] for k in properties if k != "code"}
        )


def process_csv(csv_file, geojson_data, skip_rows, key_mapping):
    print(f"Processing CSV file: {csv_file} with skip_rows: {skip_rows}")
    modified_geojson_data = copy.deepcopy(geojson_data)
    properties_by_code = {}

    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        for _ in range(skip_rows):
            next(csv_reader)
        header = next(csv_reader)
        print(f"CSV Header: {header}")

        for row in csv_reader:
            if len(row) > 0 and row[0].startswith("S"):
                row = [0 if cell == "-" else cell for cell in row]
                properties = dict(zip(header, row))
                code = row[0]  # Assuming the first column is always the code
                properties_by_code[code] = {
                    key_mapping[k]: properties[k] for k in properties if k != "code"
                }

    print(f"Processing .geojson file for: {csv_file}")
    for key in ["intersected", "output_areas"]:
        code_key = "code_2" if key == "intersected" else "code"
        for feature in modified_geojson_data[key]["features"]:
            feature_code = feature["properties"].get(code_key)
            if feature_code in properties_by_code:
                feature["properties"] = properties_by_code[feature_code]

    return modified_geojson_data


def main():
    intersected_geojson = load_geojson("output/intersected.geojson")
    output_areas_geojson = load_geojson("data/output-areas.geojson")
    geojson_data = {
        "intersected": intersected_geojson,
        "output_areas": output_areas_geojson,
    }

    key_mapping = create_key_mapping(csv_files)

    with open("output/key_mapping.json", "w") as file:
        ujson.dump(key_mapping, file, indent=2)

    for csv_file, skip_rows, output_name in csv_files:
        updated_geojson_data = process_csv(
            csv_file, geojson_data, skip_rows, key_mapping
        )
        save_geojson(
            updated_geojson_data["intersected"],
            f"output/intersected/scottish-intersected-{output_name}.geojson",
        )
        save_geojson(
            updated_geojson_data["output_areas"],
            f"output/output-areas/scottish-areas-{output_name}.geojson",
        )

    print("Processing completed.")


if __name__ == "__main__":
    main()
