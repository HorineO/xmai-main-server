import csv

file_name = "users.csv"

with open(file_name, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["UID", "PIN", "ACTIVE", "IDENTITY", "CHECKED_IN_DATES"])


with open(file_name, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["admin", "moerkali33", True, "admin", "0000"])
    writer.writerow(["teacher", "toerkali33", True, "teacher", "0000"])
    for i in range(2022, 2026):
        for j in range(1, 10):
            for k in range(1, 65):
                uidin = str(i) + str(j).zfill(2) + str(k).zfill(2)
                writer.writerow(
                    [uidin, str(i * j * k).zfill(7), True, "student", "0000"]
                )
