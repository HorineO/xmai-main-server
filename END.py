from flask import jsonify
import os
import csv


def show_csv(cclass):
    csv_file = "./instance/users.csv"
    with open(csv_file, "r") as file:
        csv_content = file.read().splitlines()
    headers = csv_content[0].split(",")
    rows = [row.split(",") for row in csv_content[1:]]
    data = []
    for row in rows:
        row_data = dict(zip(headers, row))
        if row_data["UID"][:-2] == cclass:
            data.append({key: row_data[key] for key in ["UID", "CHECKED_IN_DATES"]})
    return jsonify(data)


def change_file_extension(file_path, new_extension):
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}{new_extension}"
    new_file_path = os.path.join(directory, new_filename)
    os.rename(file_path, new_file_path)
    return new_file_path


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return 1
    else:
        return 0
