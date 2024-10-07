import csv
import concurrent.futures


def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        return {int(row[0]): row[1] for row in reader}


def grade_answers(answer_sheet, answers):
    score = 0
    for question_number, answer in answer_sheet.items():
        if question_number in answers and answer == answers[question_number]:
            score += 1
    return score


def grade_answer_sheet(answer_sheet_path, answers_path):
    try:
        # Multithreading to read the CSV files
        with concurrent.futures.ThreadPoolExecutor() as executor:
            answer_sheet_future = executor.submit(read_csv, answer_sheet_path)
            answers_future = executor.submit(read_csv, answers_path)
            answer_sheet = answer_sheet_future.result()
            answers = answers_future.result()
        return grade_answers(answer_sheet, answers)
    except Exception as e:
        return str(e)

