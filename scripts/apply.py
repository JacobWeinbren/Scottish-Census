import os
import csv
import ujson
import copy
from dictionary import create_key_mapping


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

    code_key = "code_2" if "intersected" in modified_geojson_data else "code"

    print(f"Processing .geojson file for: {csv_file}")
    for key in ["intersected", "output_areas"]:
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
    csv_files = [
        ("output/census_ages.csv", 0, "ages"),
        ("data/census-data/UV201 - Ethnic group.csv", 4, "ethnic-group"),
        ("data/census-data/UV202 - National Identity.csv", 4, "national-identity"),
        (
            "data/census-data/UV203 - Multiple ethnic groups.csv",
            3,
            "multiple-ethnic-groups",
        ),
        ("output/census_nationalities.csv", 0, "nationalities"),
        ("data/census-data/UV205 - Religion.csv", 4, "religion"),
        ("data/census-data/UV206 - Passports held.csv", 4, "passports-held"),
        (
            "data/census-data/UV208 - Gaelic language skills.csv",
            4,
            "gaelic-language-skills",
        ),
        (
            "data/census-data/UV209 - Scots language skills.csv",
            4,
            "scots-language-skills",
        ),
        (
            "data/census-data/UV210 - English language skills.csv",
            4,
            "english-language-skills",
        ),
        (
            "data/census-data/UV211 - British Sign Language (BSL) skills.csv",
            4,
            "bsl-skills",
        ),
        ("data/census-data/UV212 - Main language.csv", 4, "main-language"),
        ("data/census-data/UV406 - Household size.csv", 3, "household-size"),
    ]

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
