import sys
import os
import re
import csv
from pathlib import Path
import configparser

if (len(sys.argv)<=2):
    str = ("Read .csv and remove specified field \n"
            "Usage:\n"
            "   py {} [InCsv] [OutCsv]\n"
            .format(os.path.basename(__file__))
    )
    print(str)
    sys.exit()

strInFolder = sys.argv[1]
strOutFolder = sys.argv[2]
# strExclFields = sys.argv[3]
# rgExclFields = strExclFields.split(",")

config = configparser.ConfigParser()
config.read("RemoveCsvFields.ini")
# Access values
strExclFields = config["csv"]["ExclFields"]
rgExclFields = strExclFields.split(",")
# strDblQuoteFields = config["csv"]["DblQuoteFields"]
# rgDblQuoteFields = strDblQuoteFields.split(",")


def clone_directory_structure(src_root, dst_root):
    src = Path(src_root)
    dst = Path(dst_root)

    for path in src.rglob("*"):
        if path.is_dir():
            rel = path.relative_to(src)
            (dst / rel).mkdir(parents=True, exist_ok=True)

def list_csv_files_relative(root_folder):
    csv_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        for name in filenames:
            if name.lower().endswith(".csv"):
                full_path = os.path.join(dirpath, name)
                rel_path = os.path.relpath(full_path, root_folder)
                csv_files.append(rel_path)
    return csv_files

def force_quote(value):
    """Wrap a value in double quotes and escape internal quotes."""
    if value is None:
        return '""'
    text = str(value)
    text = text.replace('"', '""')   # escape embedded quotes
    return f'"{text}"'

def remove_fields(input_file, output_file, fields_to_remove):
    """
    Remove specified columns from a CSV file.

    :param input_file: Path to the input CSV file
    :param output_file: Path to save the cleaned CSV file
    :param fields_to_remove: List of column names to remove
    """
    #with open(input_file, "r", newline="", encoding="utf-8") as infile:
    with open(input_file, "r", newline="") as infile:
        reader = csv.DictReader(infile)
        # Determine which fields to keep
        fields_to_keep = [f for f in reader.fieldnames if f not in fields_to_remove]

        #with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        with open(output_file, "w", newline="") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fields_to_keep)
            #writer = csv.DictWriter(outfile, fieldnames=fields_to_keep, quoting=csv.QUOTE_NONE, escapechar="\\")
            writer.writeheader()

            for row in reader:
                filtered_row = {k: v for k, v in row.items() if k in fields_to_keep}
                writer.writerow(filtered_row)

            # for row in reader:
            #     filtered_row = {k: v for k, v in row.items() if k in fields_to_keep}
            #     new_row = filtered_row.copy()
            #     for col in rgDblQuoteFields:
            #         if col in new_row:
            #             # Wrap in quotes manually
            #             #new_row[col] = f'"{new_row[col]}"'
            #             new_row[col] = force_quote(new_row[col])
            #     writer.writerow(new_row)


clone_directory_structure(strInFolder, strOutFolder)

files = list_csv_files_relative(strInFolder)
for f in files:
    src = strInFolder + "\\" + f
    dest = strOutFolder + "\\" + f
    remove_fields(src, dest, rgExclFields)


# Example usage:
# remove_fields(strInCsv, strOutCsv, rgExclFields)

