from flask import Flask, render_template


def show_csv():
    # 假设你的CSV文件名为data.csv，并且位于当前目录下
    csv_file = "./instance/users.csv"

    # 读取CSV文件内容
    with open(csv_file, "r") as file:
        csv_content = file.read().splitlines()

    # 获取CSV文件的列名
    headers = csv_content[0].split(",")

    # 获取CSV文件的数据行
    rows = [row.split(",") for row in csv_content[1:]]

    # 渲染HTML模板
    return render_template("teacher.html", headers=headers, rows=rows)
