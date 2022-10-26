import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('3P-MedicalSurvey')

# Crear un objeto llamado question en el que poner condiciones de validación, 
# la pregunta y lista con opciones de respuesta y hacer una lista de los 
# objetos pregunta para poder triggearlas solo con el index(variable global 
# que aumenta cada vez que el usuario responde a una pregunta con un valor correcto).
# report


class Question:
    """
    Question class that contains the type of validation used for the specific 
    question and its answers in case it has multiple options.
    """
    def __init__(self, question, valid, answers, final_answer):
        self.question = question
        self.valid = valid
        self.answers = answers
        self.final_answer = final_answer


question_list = [
    Question("What is your first name?", "text", [], ""),
    Question("What is your last name?", "text", [], ""),
    Question("What is your blood type?", "options", ["1. A+", "2. A-", "3. B+", "4. B-", "5. O+", "6. O-", "7. AB+", "8. AB-"], ""),
    Question("How healthy do you consider yourself on a scale of 1 to 10?", "options", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], ""),
    Question("How often do you get a health checkup?", "options", ["1. Once in 3 months", "2. Once in 6 months", "3. Only when needed", "4. Never get done"], ""),
    Question("Do you have any chronic diseases?", "y/n", [], ""),
    Question("Do you have any hereditary conditions/diseases?", "options", ["1. High blood pressure", "2. Diabetes", "3. Hemophilia", "4. Thalassemia", "5. Huntington", "6. Other"], ""),
    Question("How often do you consume alcohol?", "options", ["1. I don't drink", "2. Only occasionally", "3. Two/three times a week", "4. More than two/three times a week"], ""),
    Question("How often do you consume cigarettes?", "options", ["1. I don't smoke", "2. Only occasionally", "3. One pack a week", "4. More than one pack a week"], ""),
    Question("Do you consume other drugs?", "options", ["1. I don't consume other drugs", "2. Only occasionally", "3. Two/three times a week", "4. More than two/three times a week"], ""),
    Question("Over the past 2 weeks, how often have you felt nervous, anxious, or on edge?", "options", ["1. Not all", "2. Several days", "3. More days than not", "4. Nearly every day"], ""),
    Question("Over the past 2 weeks, how often have you felt down, depressed, or hopeless?", "options", ["1. Not all", "2. Several days", "3. More days than not", "4. Nearly every day"], ""),
    Question("Over the past 2 weeks, how often have you felt little interest or pleasure in doing things?", "options", ["1. Not all", "2. Several days", "3. More days than not", "4. Nearly every day"], ""),
    Question("How would you describe the condition of your mouth and teeth, including false teeth or dentures?", "options", ["1. Excellent", "2. Good", "3. Average", "4. Poor"], ""),
    Question("How often do you practice some exercise a week?", "options", ["1. More than 4 days a week", "2. 3-4 days a week", "3. 1-2 days a week", "4. Never"], ""),
]


def question_trigger(current_question):
    """
    Shows the question to the user and get his input.
    """
    print(current_question.question)
    if current_question.valid == "text":
        user_answer = input("\n\n")
        if question_validation(user_answer, current_question):
            print("The answer is valid!")
            return True
        else:
            return False
    elif current_question.valid == "options":
        option_str = "  ".join(current_question.answers)
        user_answer = input(option_str + "\n\n")
        if question_validation(user_answer, current_question):
            print("The answer is valid!")
            return True
        else:
            return False
    elif current_question.valid == "y/n":
        user_answer = input("Please answer YES or NO: \n\n")
        if question_validation(user_answer, current_question):
            print("The answer is valid!")
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
            print("You entered an invalid answer, please use only alphabetic characters. \n")
            return False
    elif question_to_validate.valid == "options":
        if answer.isnumeric() is True and int(answer) <= len(question_to_validate.answers) and int(answer) > 0:
            question_to_validate.final_answer = question_to_validate.answers[int(answer) - 1]
            return True
        else:
            print("Please choose one of the following options using the numeric values assigned. \n")
            return False
    elif question_to_validate.valid == "y/n":
        if answer.lower() == "yes" or answer.lower() == "no":
            question_to_validate.final_answer = answer
            return True
        else:
            print("Please answer only YES or NO. \n")
            return False


def update_data_sheet():
    """
    Updates the spreadsheet with the answers given by the user.
    """
    all_answers = []
    for ind in question_list:
        all_answers.append(ind.final_answer)
    SHEET.worksheet("data").append_row(all_answers)
    print("Data worksheet updated")
    

def main():
    """
    Run all program functions.
    """
    print("Welcome to our medical survey. Please answer truthfully to the following questions:\n")
    for ind in question_list:
        is_valid = False
        while is_valid is False:
            is_valid = question_trigger(ind)
    
    update_data_sheet()


main()
