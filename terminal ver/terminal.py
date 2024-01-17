import requests

#parameters for the questions taken from Open Trivia Database
parameters = {
    #10 questions
    "amount": 10,
    #type of questions is multiple choice
    "type": "multiple"
}

#HTTP GET request to Open Trivia Database with the parameters for the questions
response = requests.get(url="https://opentdb.com/api.php", params=parameters)

var_response_question_data = response.json()["results"]



#class "Question"
class Question:
    #question and correct_answer are strings and the choices are a list
    def __init__(self, question: str, correct_answer: str, choices: list):
        #assigns the value of "question, correct_answer and choices" to respective variables
        self.question_text = question
        self.correct_answer = correct_answer
        self.choices = choices


#class "Quiz_operation"
class Quiz_operation:
    def __init__(self, questions):
        self.question_no = 0
        self.score = 0
        self.questions = questions
        self.current_question = None

    


    def has_more_questions(self):
        return self.question_no < len(self.questions)

    def next_question(self):
        self.current_question = self.questions[self.question_no]
        self.question_no += 1
        ques_text = self.current_question.question_text
        return f"Q.{self.question_no}: {ques_text}"


    def check_answer(self, user_answer):
        
        correct_answer = self.current_question.correct_answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False

    def get_score(self):
        wrong = self.question_no - self.score
        score_percent = int(self.score / self.question_no * 100)
        return (self.score, wrong, score_percent)


#note: while loop is used for terminal and for loop for tkinter


def display_choices(choices):
        for index, choice in enumerate(choices, start=1):
            print(f"{index}. {choice}")

'''test in the terminal'''

#  Create an instance of the Quiz_operation class with the question data
quiz = Quiz_operation([Question(q["question"], q["correct_answer"], q["incorrect_answers"]) for q in var_response_question_data])

# Start the quiz
print("Welcome to the Quiz!")
print("Answer the following questions:")
while quiz.has_more_questions():
    print()
    question_text = quiz.next_question()
    print(question_text)

    # Display answer choices
    display_choices(quiz.current_question.choices)

    # Take user input
    user_choice = input("Enter the number corresponding to your choice: ")

    # Validate user input
    if not user_choice.isdigit() or not (1 <= int(user_choice) <= len(quiz.current_question.choices)):
        print("Invalid input. Please enter a valid number.")
        continue

    # Check user's answer
    user_answer = quiz.current_question.choices[int(user_choice) - 1]
    if quiz.check_answer(user_answer):
        print("Correct!")
    else:
        print(f"Incorrect! The correct answer was: {quiz.current_question.correct_answer}")

# Quiz finished, display score
score, wrong, score_percent = quiz.get_score()
print()
print("Quiz finished!")
print(f"Your score: {score}/{score + wrong} ({score_percent}%)")




print("You've completed the quiz")
#displays the user's final score
#quiz.score divided by quiz.question_no
print(f"Your final score was: {quiz.score}/{quiz.question_no}")
#prints this in the terminal not window