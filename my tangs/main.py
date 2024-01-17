import requests
from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox, font
import customtkinter as ctk
import html



THEME_COLOR = "#4f3762"




#parameters for the questions taken from Open Trivia Database
parameters = {
    #10 questions
    "amount": 10,
    #type of questions is multiple choice
    "type": "multiple"
}

#HTTP GET request to Open Trivia Database with the parameters for the questions
response = requests.get(url="https://opentdb.com/api.php", params=parameters)

#response.json() --  converts the data from JSON format to Python dictionary
#results -- contains/exracts all the questions
#var_response_question_data --data from json assigned to this variable

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
    #function
    def __init__(self, questions):
        #variable for the count  of the questions /will be used later to see which numext_questiober you are on
        self.question_no = 0
        #variable to count the score
        self.score = 0
        #note: the value of the "questions" parameter is a list from "question_bank_list"
        #assigns the value of the "questions" parameter to variable "self.questions" 
        self.questions = questions
        #variable to store the current question which starts wiith no curret question because of none
        self.current_question = None

    #Function to check if the quiz has more questions to answer
    def has_more_questions(self):
        #note: the value of the "questions" parameter is a list from "question_bank_list"
        #if question_no is less than the length of the "self.questions" from the __init__, then return true
        return self.question_no < len(self.questions)

    def next_question(self):
        #Get the next question by incrementing the question number
        #"self.current_question" starts with no curret question because of none
        #"self.question_no" asigns the value of the current question in "self.questions" to what ever value of "self.question_no" is at the time
        self.current_question = self.questions[self.question_no]
        #increment by 1 the value of the number question "self.question_no"
        self.question_no += 1
        #assigns the value of the "self.current_question.question_text" to "ques_text"
        #ques_text variable is used to store the current question text for each question in the quiz
        #self.current_question.question_text retrieve and use the text of the current question
        ques_text = self.current_question.question_text
        #returns the current value in "question_no"(question number) and ques_text(current question text) from Question
        return f"Q.{self.question_no}: {ques_text}"

    #funtion to check the user's answer against the correct answer and maintain the score
    def check_answer(self, user_answer):
        
        correct_answer = self.current_question.correct_answer
        #if "user_answer" is equal to the value in "correct_answer" then add 1 to the "score"
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            #True or False return value determines if the answer is correct or not becasue it's going to be shown
            return True
        else:
            return False

    #funtion to get the number of correct answers, wrong answers, and score percentage
    def get_score(self):
        #To get amount of wrong answers
        #variable "wrong" is equal to the value of "self.question_no" minus the value of "self.score"
        wrong = self.question_no - self.score
        #To get the score percentage
        #variable "score_percent" is equal to the value of "self.score" divided by the value of "self.question_no" times 100 to get the percentage
        score_percent = int(self.score / self.question_no * 100)
        #returns the number of correct answers, wrong answers, and score percentage
        return (self.score, wrong, score_percent)





'''test in the terminal'''

#  Create an instance of the Quiz_operation class with the question data
# quiz = Quiz_operation([Question(q["question"], q["correct_answer"], q["incorrect_answers"]) for q in var_response_question_data])

#  Start the quiz
# print("Welcome to the Quiz!")
# print("Answer the following questions:")

# while quiz.has_more_questions():
#     print()
#     question = quiz.next_question()
#     print(question)

#     user_answer = input("Your answer: ")
#     if quiz.check_answer(user_answer):
#         print("Correct!")
#     else:
#         print("Incorrect!")

#  Quiz finished, display score
# score, wrong, score_percent = quiz.get_score()
# print()
# print("Quiz finished!")
# print(f"Your score: {score}/{score + wrong} ({score_percent}%)")


'''test in the terminal'''












#class "Quiz_Tkinter_Interface"
class Quiz_Tkinter_Interface:
    #this class is created for the tkinter inerface
    def __init__(self, quiz_brain):
        self.quiz = quiz_brain
        self.window = Tk()
        #title of the window
        self.window.title("Trivia App")
        #size of the window
        self.window.geometry("650x530")

        #Display Title
        self.display_title()

        #Create a canvas for question text,  dsiplay question
        #Size of canvas with  border/border weight 3 and relief solid
        self.canvas = Canvas(width=500, height=130, border= 3, relief= "solid")
        #"200,65" x and y position on the canvas
        self.question_text = self.canvas.create_text(200, 65,
                                                     #filler text for canvas
                                                     text="Question here",
                                                     #"Question here" text is wrapped within a width of 380px
                                                     width=380,
                                                     #text color is from variable "THEMEE_COLOR" 
                                                     fill=THEME_COLOR,
                                                     #font | font size | font style
                                                     font=(
                                                         'Arial', 15, 'bold')
                                                     )
        #pady=70 is the space on top of the canvas
        self.canvas.pack(pady=70)
        self.display_question()

        #Declare a StringVar to store user's answer
        self.user_answer = StringVar()

        #Display four options (radio buttons)
        self.opts = self.radio_buttons()
        self.display_options()

        #the text that shows if answer is right or wrong
        #pady=5 is the space on top of the label and bottom of the label and font | font size | font style
        self.feedback = Label(self.window, pady=5, font=("Arial", 15, "bold"))
        #placement of the label
        self.feedback.place(x=90, y=380)

        #Next and Quit Button
        self.buttons()

        #Mainloop
        self.window.mainloop()


    #To display title
    def display_title(self):

        #Title label with text "Trivia Application"
        title = Label(self.window, text="Trivia Application",
                      #size of the title |backgruound nad foregroud color | font | font size | font style
                      width=30, bg=THEME_COLOR, fg="white", font=("Arial", 30, "bold"))

        # place of the title with x and y positiong
        title.place(x=0, y=2)

    #To display the question
    def display_question(self):
        #variable q_text is variable that takes the next_question() function from "quiz" which is Quiz_operation
        q_text = self.quiz.next_question()
        #itemconfig adds the question in the canvas replacing the text from "Question here" into variable "q_text"
        self.canvas.itemconfig(self.question_text, text=q_text)

    #To create four options (radio buttons)
    def radio_buttons(self):
        

        #initialize the list with an empty list of options
        #where the list of choice will be appended
        choice_list = []

        #position of the first option
        y_pos = 220

        #Adding the options to the list
        while len(choice_list) < 4:

            #Radio button properties
            #when the user selects an option the value in "user_answer" will be updated
            radio_btn =Radiobutton(self.window, text="", variable=self.user_answer,
                                    value='', font=("Arial", 14))
            


            #adding the button to the list
            choice_list.append(radio_btn)

            # placing the button
            radio_btn.place(x=100, y=y_pos)

            #incrementing the y-axis position by 40 so the choices aren't on top of each other
            y_pos += 40

        #return the radio buttons
        return choice_list
        #In each iteration of the while loop, a new Radiobutton widget is created

    #To display four options
    def display_options(self):
        

        val = 0

        #Deselects any previously selected option by setting the "user_answer" variable (which is a StringVar) to None
        self.user_answer.set(None)

        #looping over the options to be displayed for the text of the radio buttons.
        #Loop over the options in the "current_question" variable from choices list at the bottom
        #For each option in the list of choices for the current question Update the text and value of the radio buttons
        for option in self.quiz.current_question.choices:
            #self.opts is a list containing the radio buttons
            #text = Sets the text displayed on the radio button to the current option
            self.opts[val]['text'] = option
            #value = The value is what is stored in the StringVar (user_answer)
            #self.opts[val] is used to access the specific radio button at index val in the list of radio buttons.
            self.opts[val]['value'] = option
            #next iteration of the loop will update the next radio button in the list.
            val += 1

    #To show feedback for each answer and keep checking for more questions
    def next_btn(self):
        
        # Check if the answer is correct
        if self.quiz.check_answer(self.user_answer.get()):
            #right asnwer
            self.feedback["fg"] = "green"
            self.feedback["text"] = 'Correct!'
        else:
            #wrong answer
            self.feedback['fg'] = 'red'
            self.feedback['text'] = ('wrong! \n'
                                     f'The right answer is: {self.quiz.current_question.correct_answer}')

        if self.quiz.has_more_questions():
            #next to display next question and its options
            self.display_question()
            self.display_options()
        else:
            #if no more questions, then it displays the score
            self.display_result()

            #destroys the self.window
            self.window.destroy()

    def buttons(self):
        """To show next button and quit button"""

        #The first button is the Next button to move to the
        #next Question
        next_button =ctk.CTkButton(self.window, text="Next", command=self.next_btn,
                             width=100,height=10, hover_color=THEME_COLOR,fg_color="green", font=("Arial", 20, "bold"))

        #palcing the button on the screen
        next_button.place(x=70, y=460)

        #This is the second button which is used to Quit the self.window
        quit_button =ctk.CTkButton(self.window, text="Quit", command=self.window.destroy,
                             width=100,height=10, hover_color=THEME_COLOR,fg_color="red", corner_radius=5, font=("Arial", 20, "bold"))

        #placing the Quit button on the screen0
        quit_button.place(x=500, y=460)

    #To display the result using messagebox
    def display_result(self):
        
        #get correct, wrong, score_percent from quiz(Quiz_operation)
        correct, wrong, score_percent = self.quiz.get_score()

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        #displays the correct answer from getscore()
        result = f"Score: {score_percent}%"

        #Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")


#for loop
#empty list called question_bank_list where Question objects will be stored.
question_bank_list = []
#iterates through each question in the var_response_question_data obtained from the API response.
for question in var_response_question_data:
    choices = []
    #decodes HTML entities in the question text and correct answer / html.unescape Converts "&quot;"" to ""
    question_text = html.unescape(question["question"]) 
    correct_answer = html.unescape(question["correct_answer"])
    #takes incorrect answers and appends the incorrect answers to the choices list
    incorrect_answers = question["incorrect_answers"]
    for ans in incorrect_answers:
        choices.append(html.unescape(ans))
    #appends the correct answer to the choices list
    choices.append(correct_answer)
    
    #creates a new Question object with the decoded question text, correct answer, and the list of choices
    new_question = Question(question_text, correct_answer, choices)
    #Question object is added to the question_bank_list list
    question_bank_list.append(new_question)


quiz = Quiz_operation(question_bank_list)
#Quiz_operation class, passing the question_bank_list list to initialize the quiz with the set of questions.

quiz_ui = Quiz_Tkinter_Interface(quiz)
#Creates an instance of the Quiz_Tkinter_Interface class, passing the initialized Quiz_operation instance to create the graphical user interface for the quiz.

print("You've completed the quiz")
#displays the user's final score
#quiz.score divided by quiz.question_no
print(f"Your final score was: {quiz.score}/{quiz.question_no}")
#prints this in the terminal not window