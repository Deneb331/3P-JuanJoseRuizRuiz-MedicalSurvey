import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("3P-MedicalSurvey")


class Question:
    """
    Question class that contains the type of validation used for the specific
    question and its answers in case it has multiple options.
    """

    def __init__(
        self, question, valid, answers, final_answer, report_type, report_data
    ):
        self.question = question
        self.valid = valid
        self.answers = answers
        self.final_answer = final_answer
        self.report_type = report_type
        self.report_data = report_data


question_list = [
    Question("What is your first name?", "text", [], "", "", ""),
    Question("What is your last name?", "text", [], "", "", ""),
    Question(
        "What is your blood type?",
        "options",
        ["1. A+", "2. A-", "3. B+", "4. B-", "5. O+", "6. O-", "7. AB+", "8. AB-"],
        "",
        "%",
        "",
    ),
    Question(
        "How healthy do you consider yourself on a scale of 1 to 10?",
        "options",
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        "",
        "average",
        "",
    ),
    Question(
        "How often do you get a health checkup?",
        "options",
        [
            "1. Once in 3 months",
            "2. Once in 6 months",
            "3. Only when needed",
            "4. Never get done",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "Do you have any chronic diseases?", "options", ["1. Yes", "2. No"], "", "%", ""
    ),
    Question(
        "Do you have any hereditary conditions/diseases?",
        "options",
        [
            "1. High blood pressure",
            "2. Diabetes",
            "3. Hemophilia",
            "4. Thalassemia",
            "5. Huntington",
            "6. Other",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "How often do you consume alcohol?",
        "options",
        [
            "1. I don't drink",
            "2. Only occasionally",
            "3. Two/three times a week",
            "4. More than two/three times a week",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "How often do you consume cigarettes?",
        "options",
        [
            "1. I don't smoke",
            "2. Only occasionally",
            "3. One pack a week",
            "4. More than one pack a week",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "Do you consume other drugs?",
        "options",
        [
            "1. I don't consume other drugs",
            "2. Only occasionally",
            "3. Two/three times a week",
            "4. More than two/three times a week",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "Over the past 2 weeks, how often have you felt nervous, anxious, or on edge?",
        "options",
        [
            "1. Not all",
            "2. Several days",
            "3. More days than not",
            "4. Nearly every day",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "Over the past 2 weeks, how often have you felt down, depressed, or hopeless?",
        "options",
        [
            "1. Not all",
            "2. Several days",
            "3. More days than not",
            "4. Nearly every day",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "Over the past 2 weeks, how often have you felt little interest or pleasure in doing things?",
        "options",
        [
            "1. Not all",
            "2. Several days",
            "3. More days than not",
            "4. Nearly every day",
        ],
        "",
        "%",
        "",
    ),
    Question(
        "How would you describe the condition of your mouth and teeth, including false teeth or dentures?",
        "options",
        ["1. Excellent", "2. Good", "3. Average", "4. Poor"],
        "",
        "%",
        "",
    ),
    Question(
        "How often do you practice some exercise a week?",
        "options",
        [
            "1. More than 4 days a week",
            "2. 3-4 days a week",
            "3. 1-2 days a week",
            "4. Never",
        ],
        "",
        "%",
        "",
    ),
]

first_question = Question(
    "Welcome to our medical survey. What would you like to do? \n",
    "options",
    [
        "1. Do the survey",
        "2. See the report"
    ],
    "",
    "",
    "")


def question_trigger(current_question):
    """
    Shows the question to the user and get his input.
    """
    print(current_question.question)
    if current_question.valid == "text":
        user_answer = input("\n\n")
        if question_validation(user_answer, current_question):
            return True
        else:
            return False
    elif current_question.valid == "options":
        option_str = "  ".join(current_question.answers)
        user_answer = input(option_str + "\n\n")
        if question_validation(user_answer, current_question):
            return True
        else:
            return False


def question_validation(answer, question_to_validate):
    """
    Validates the answer given by the user. If it is valid, let the program
    continue. If it's not, make the user answer again.
    """
    if question_to_validate.valid == "text":
        if answer.isalpha() is True:
            question_to_validate.final_answer = answer
            return True
        else:
            print(
                "You entered an invalid answer, please use only alphabetic characters. \n"
            )
            return False
    elif question_to_validate.valid == "options":
        if (
            answer.isnumeric() is True
            and int(answer) <= len(question_to_validate.answers)
            and int(answer) > 0
        ):
            question_to_validate.final_answer = int(answer) - 1
            return True
        else:
            print(
                "Please choose one of the following options using the numeric values assigned. \n"
            )
            return False


def update_data_sheet():
    """
    Updates the spreadsheet with the answers given by the user.
    """
    all_answers = []
    for ind in question_list:
        if ind.valid == "text" or ind.valid == "y/n":
            all_answers.append(ind.final_answer)
        else:
            all_answers.append(ind.answers[int(ind.final_answer)])
    SHEET.worksheet("data").append_row(all_answers)
    print("Data worksheet updated")


def generate_report():
    """
    Generates a report with all the data stored in the sheet and
    shows the report to the user.
    """
    print("Generating report data...\n")
    data = SHEET.worksheet("data")
    rows = []
    for ind in range(2, data.row_count + 1):
        row = data.row_values(ind)
        del row[0]
        del row[0]
        rows.append(row)
    for i in question_list:
        if i.report_type == "%":
            data_list = []
            for j in rows:
                for k in i.answers:
                    if k in j:
                        data_list.append(k)
            for unit in i.answers:
                if data_list.count(unit) == 0:
                    continue
                percentage = round(data_list.count(unit) * 100 / len(data_list), 2)
                i.report_data += unit + " " + str(percentage) + "%  "
            print(i.question + ": \n" + i.report_data + "\n")


def main():
    """
    Run all program functions.
    """
    while True:
        choice = question_trigger(first_question)
        if choice:
            if int(first_question.final_answer) + 1 == 1:
                print("Welcome to the survey. Please, answer the questions truthfully: \n")
                for ind in question_list:
                    is_valid = False
                    while is_valid is False:
                        is_valid = question_trigger(ind)
                update_data_sheet()
                return False
            elif int(first_question.final_answer) + 1 == 2:
                generate_report()
                return False
            else:
                print("Please enter a valid option.")
        else:
            print("Please enter a valid option. \n")


if __name__ == "__main__":
    main()
