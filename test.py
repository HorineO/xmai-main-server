csv_file = "./instance/users.csv"

cclass = "202201"

with open(csv_file, "r") as file:
    csv_content = file.read().splitlines()

headers = csv_content[0].split(",")
rows = [row.split(",") for row in csv_content[1:]]

data = []
for row in rows:
    row_data = dict(zip(headers, row))
    if row_data["UID"][:-2] == cclass:
        data.append(row_data)
print(data)
# print(data[2]["UID"][:-2] == cclass)
