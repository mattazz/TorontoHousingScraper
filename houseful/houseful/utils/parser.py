import json
import re


def parse_zolo_json(data: str) -> dict:
    # Remove the variable assignment part to get just the JSON-like string
    data = re.sub(r"var ZOLO_DATA = ", "", data).strip()

    # Properly escape backslashes before manipulating the string further
    data = data.replace("\\", "\\\\")

    # Add double quotes around the keys
    data = re.sub(
        r'(?<!\\)"', "'", data
    )  # Temporarily replace unescaped double quotes with single quotes
    data = re.sub(
        r"([\{\s,])(\w+)(\s*:)", r'\1"\2"\3', data
    )  # Add double quotes around the keys
    data = data.replace("'", '"')  # Revert single quotes back to double quotes

    # Load the string as a JSON object
    data_dict = json.loads(data)
    print(data_dict)
    return data_dict


def csv_remove_blanks():
    with open("../../links.csv", "r") as f:
        lines = f.readlines()

    # Remove blank lines
    lines = [line for line in lines if line.strip() != ""]

    with open("links.csv", "w") as f:
        f.writelines(lines)


def csv_to_list(path: str):
    list = []
    with open(path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        list.append(line)

    return list
