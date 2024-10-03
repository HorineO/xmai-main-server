import csv


class Add_Users:
    def __init__(self, uid, pin, active, file_name):
        self.uid = uid
        self.pin = pin
        self.active = active
        self.file_name = file_name

    # read and write CSV file
    try:

        def add(self):
            with open(self.file_name, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([self.uid, self.pin, self.active])

    except SyntaxError:
        print("Syntax Error\n maybe you have entered wrong char types")
        pass


class Direct_Spesify:
    def __init__(self, file_name, content, row, column):
        self.content = content
        self.file_name = file_name
        self.row = row
        self.column = column

    try:

        def spesify(self):
            # read CSV file
            with open(self.file_name, "r", newline="") as file:
                reader = csv.reader(file)
                data = list(reader)
            # revise the data
            data[self.row][self.column] = self.content
            # write the modified data
            with open(self.file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(data)

    except SyntaxError:
        print("Syntax Error\n maybe you have entered wrong char types")
        pass


class Row_Specify:
    def __init__(self, file_name, row, content):
        self.file_name = file_name
        self.row = row
        self.content = content

    try:

        def specify(self):
            with open(self.file_name, "r", newline="") as file:
                reader = csv.reader(file)
                data = list(reader)
            data[self.row] = self.content
            with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)

    except SyntaxError:
        print("Syntax Error\n maybe you have entered wrong char types")
        pass


class Init_File:
    def __init__(self, file_name):
        self.file_name = file_name
        with open(self.file_name, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["UID", "PIN", "ACTIVE", "IDENTITY", "CHECKED_IN_DATES"])


class Identity:
    def __init__(self, file_name, uid, identity):
        self.file_name = file_name
        self.uid = uid
        self.identity = identity

    def back(self):
        with open(self.file_name, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if self.uid in row:
                    if row[1] == self.identity:
                        if row[2] == "True":
                            if row[3] == "admin":
                                return 1
                            elif row[3] == "teacher":
                                return 2
                            elif row[3] == "student":
                                return 3
            return 0


class Users_Checkin:
    def __init__(self, file_name, uid, date):
        self.file_name = file_name
        self.uid = uid
        self.date = date

    def checkin(self):
        with open(self.file_name, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            data = list(reader)

        for i, row in enumerate(data):
            if row[0] == str(self.uid) and self.date not in data[i][4]:
                data[i][4] = f"{self.date},{data[i][4]}"
            # print(row[0])

        with open(self.file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
