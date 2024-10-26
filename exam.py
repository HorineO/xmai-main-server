from flask import jsonify
import csv
import concurrent.futures


def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        return {int(row[0]): row[1] for row in reader}


def grade_answers(answers, student_answers):
    score = 0
    for question, correct_answer in answers.items():
        if student_answers.get(question) == correct_answer[1]:
            score += int(correct_answer[0])
    return score


def grade_answer_sheet(answer_sheet_path, answers_path, accuracy=False):
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            answer_sheet_future = executor.submit(read_csv, answer_sheet_path)
            answers_future = executor.submit(read_csv2, answers_path)
            answer_sheet = answer_sheet_future.result()
            answers = answers_future.result()

        score = sum(
            1
            for question_number, answer in answer_sheet.items()
            if question_number in answers and answer == answers[question_number][1]
        )
        if accuracy:
            total_questions = len(answer_sheet)
            return score / total_questions if total_questions else 0
        return score
    except Exception as e:
        return str(e)


def read_csv2(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        return {int(row[0]): [int(row[1]), row[2]] for row in reader}


def show_csv(fclass):
    csv_file = "./instance/users.csv"
    with open(csv_file, "r") as file:
        csv_content = file.read().splitlines()
    headers = csv_content[0].split(",")
    rows = [row.split(",") for row in csv_content[1:]]
    data = []
    for row in rows:
        row_data = dict(zip(headers, row))
        if row_data["UID"][:-2] == fclass:
            data.append({key: row_data[key] for key in ["UID", "CHECKED_IN_DATES"]})
    return jsonify(data)
