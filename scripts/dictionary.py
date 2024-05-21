import csv
import string

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
}


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
