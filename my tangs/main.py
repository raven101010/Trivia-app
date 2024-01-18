import requests
from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox, font
import customtkinter as ctk
import html



THEME_COLOR = "#4f3762"




#parameters for the quests taken from Open Trivia Database
parameters = {
    #10 quests
    "amount": 10,
    #type of quests is multiple choice
    "type": "multiple"
}

#HTTP GET request to Open Trivia Database with the parameters for the quests
response = requests.get(url="https://opentdb.com/api.php", params=parameters)

#response.json() --  converts the data from JSON format to Python dictionary
#results -- contains/exracts all the quests
#opentrivia_respose_data --data from json assigned to this variable

opentrivia_respose_data = response.json()["results"]



#class "Question"
class Question:
    #question and correct_answer are strings and the options are a list
    def __init__(self, question: str, correct_answer: str, options: list):
        #assigns the value of "question, correct_answer and options" to respective variables
        self.question_text = question
        self.correct_answer = correct_answer
        self.options = options


#class "Quiz_operation"
class Quiz_operation:
    #function
    def __init__(self, quests):
        self.question_number = 0
        #variable to count the score
        self.score = 0
        #assigns the value of the "quests" parameter to variable self.quests
        self.quests = quests
        #variable to store the current question which starts wiith no curret question because of none
        self.current_question = None

    #Function to check if the quiz has more quests to answer
    def more_quest_left(self):
        #if question_number is less than the length of the "self.quests" from the __init__, then return true
        return self.question_number < len(self.quests)

    def next_question(self):
        #Gets the next question by indexing the list of quests with the current question number
        #assigns the value of the "question" at the current index (self.question_number) in the list of quests (self.quests) to the self.current_question attribute
        self.current_question = self.quests[self.question_number]
        #increment by 1 the value of the number question "self.question_number"
        self.question_number += 1
        #retrieves the text of the current question (self.current_question) using the attribute question_text of the Question class and assigns to ques_txt
        ques_txt = self.current_question.question_text
        #returns the current value in "question_number"(question number) and ques_txt(current question text) from Question
        return f"Q.{self.question_number}: {ques_txt}"

    #funtion to check the user's answer against the correct answer and maintain the score
    def checks_if__ans_crrt(self, user_answer):
        
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
        #variable "wrong" is equal to the value of "self.question_number" minus the value of "self.score"
        wrong = self.question_number - self.score
        #To get the score percentage
        #variable "prct_score" is equal to the value of "self.score" divided by the value of "self.question_number" times 100 to get the percentage
        prct_score = int(self.score / self.question_number * 100)
        #returns the number of correct answers, wrong answers, and score percentage
        return (self.score, wrong, prct_score)





'''test in the terminal'''

#  Create an instance of the Quiz_operation class with the question data
# quiz = Quiz_operation([Question(q["question"], q["correct_answer"], q["incorrect_answers"]) for q in opentrivia_respose_data])

#  Start the quiz
# print("Welcome to the Quiz!")
# print("Answer the following quests:")

# while quiz.more_quest_left():
#     print()
#     question = quiz.next_question()
#     print(question)

#     user_answer = input("Your answer: ")
#     if quiz.checks_if__ans_crrt(user_answer):
#         print("Correct!")
#     else:
#         print("Incorrect!")

#  Quiz finished, display score
# score, wrong, prct_score = quiz.get_score()
# print()
# print("Quiz finished!")
# print(f"Your score: {score}/{score + wrong} ({prct_score}%)")


'''test in the terminal'''












#class "Quiz_Tkinter_Interface"
class Quiz_Tkinter_Interface:
    #this class is created for the tkinter inerface
    def __init__(self, quiz_nterface):
        self.quiz = quiz_nterface
        self.window = Tk()
        #title of the window
        self.window.title("Trivia App")
        #size of the window
        self.window.geometry("650x530")

        #Display Title
        self.app_title()

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
        self.quest_show()

        #string variable for tthe anser of the user
        self.user_answer = StringVar()

        #showing thechoices
        self.opts = self.radio_buttons()
        self.answer_option_show()

        #the text that shows if answer is right or wrong
        #pady=5 is the space on top of the label and bottom of the label and font | font size | font style
        self.feedback = Label(self.window, pady=5, font=("Arial", 15, "italic"))
        #placement of the label
        self.feedback.place(x=90, y=380)

        #Next and Quit Button
        self.buttons()
        self.window.mainloop()


    #To display title
    def app_title(self):

        #Title label with text "Trivia Application"
        title = Label(self.window, text="Trivia Application",
                      #size of the title |backgruound nad foregroud color | font | font size | font style
                      width=30, bg=THEME_COLOR, fg="white", font=("Arial", 30, "bold"))

        #show the title in place with x and y positioning
        title.place(x=0, y=2)

    #To display the question
    def quest_show(self):
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
        y_pos = 230

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

            #incrementing the y-axis position by 40 so the options aren't on top of each other
            y_pos += 40

        #return the radio buttons
        return choice_list
        #In each iteration of the while loop, a new Radiobutton widget is created

    #To display four options
    def answer_option_show(self):

        val = 0

        #Deselects any previously selected option by setting the "user_answer" variable (which is a StringVar) to None
        self.user_answer.set(None)

        #loops over the options displayed for text of radio buttons.
        #Loop over the options in the "current_question" variable from options list at the bottom
        #For each option in the list of options for the current question Update the text and value of the radio buttons
        for option in self.quiz.current_question.options:
            #self.opts is a list containing the radio buttons
            #text = Sets the text displayed on the radio button to the current option
            self.opts[val]['text'] = option
            #value = The value is what is stored in the StringVar (user_answer)
            #self.opts[val] is used to access the specific radio button at index val in the list of radio buttons.
            self.opts[val]['value'] = option
            #next iteration of the loop will update the next radio button in the list.
            val += 1

    #To show feedback for each answer and keep checking for more quests
    def next_btn(self):
        
        # Check if the answer is correct
        if self.quiz.checks_if__ans_crrt(self.user_answer.get()):
            #right asnwer
            self.feedback["fg"] = "green"
            self.feedback["text"] = 'Correct!'
        else:
            #wrong answer
            self.feedback['fg'] = 'red'
            self.feedback['text'] = ('wrong! \n'
                                     f'answer is: {self.quiz.current_question.correct_answer}')

        if self.quiz.more_quest_left():
            #next to display next question and its options
            self.quest_show()
            self.answer_option_show()
        else:
            #if no more quests, then it displays the score
            self.show_score_result()

            #destroys the self.window
            self.window.destroy()

    def buttons(self):
        #next button and quit button

        #next btn =  the Next button to move to the
        #next Question
        btn_next =ctk.CTkButton(self.window, text="Next question", command=self.next_btn,
                             width=100,height=10, hover_color=THEME_COLOR,fg_color="green", font=("Arial", 20, "bold"))

        #placing the button on the screen
        btn_next.place(x=70, y=460)

        #This is the second button which is used to Quit the self.window
        btn_quit =ctk.CTkButton(self.window, text="Quit", command=self.window.destroy,
                             width=100,height=10, hover_color=THEME_COLOR,fg_color="red", corner_radius=5, font=("Arial", 20, "bold"))

        #placing the Quit button on the screen
        btn_quit.place(x=500, y=460)

    #To display the result using messagebox
    def show_score_result(self):
        
        #get correct, wrong, prct_score from quiz(Quiz_operation)
        correct, wrong, prct_score = self.quiz.get_score()

        question_got_right = f"Correct: {correct}"
        mistake = f"Wrong: {wrong}"

        #displays the correct answer from getscore()
        result_percentage = f"Score: {prct_score}%"

        #Shows a message box to display the result
        messagebox.showinfo("Result", f"{result_percentage}\n{question_got_right}\n{mistake}")


#for loop
#empty list called question_bank_list where Question objects will be stored.
question_bank_list = []
#iterates through each question in the opentrivia_respose_data obtained from the API response.
for question in opentrivia_respose_data:
    options = []
    #decodes HTML entities in the question text and correct answer / html.unescape Converts "&quot;"" to ""
    API_question_txt = html.unescape(question["question"]) 
    API_correct_ans = html.unescape(question["correct_answer"])
    #takes incorrect answers and appends the incorrect answers to the options list
    incorrect_answers = question["incorrect_answers"]
    for ans in incorrect_answers:
        options.append(html.unescape(ans))
    #appends the correct answer to the options list
    options.append(API_correct_ans)
    
    #creates a new Question object with the decoded question text, correct answer, and the list of options
    new_question = Question(API_question_txt, API_correct_ans, options)
    #Question object is added to the question_bank_list list
    question_bank_list.append(new_question)


quiz = Quiz_operation(question_bank_list)
#Quiz_operation class, passing the question_bank_list list to initialize the quiz with the set of quests.

quiz_ui = Quiz_Tkinter_Interface(quiz)
#Creates an instance of the Quiz_Tkinter_Interface class, passing the initialized Quiz_operation instance to create the graphical user interface for the quiz.

print("You've completed the quiz")
#displays the user's final score
#quiz.score divided by quiz.question_number
print(f"Your final score was: {quiz.score}/{quiz.question_number}")
#prints this in the terminal not window