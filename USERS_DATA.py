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
            writer.writerow(["UID", "PIN", "ACTIVE"])
