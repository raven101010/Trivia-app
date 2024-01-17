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


var_response_question_data = response.json()["results"]



#class "Question"
class Question:
    def __init__(self, question: str, correct_answer: str, choices: list):
        self.question_text = question
        self.correct_answer = correct_answer
        self.choices = choices


#class "Quiz_operation"
class Quiz_operation:
    #function
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
        #if "user_answer" is equal to the value in "correct_answer" then add 1 to the "score"
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            #True or False return value determines if the answer is correct or not becasue it's going to be shown
            return True
        else:
            return False

    #funtion to get the number of correct answers, wrong answers, and score percentage
    def get_score(self):
        wrong = self.question_no - self.score
        score_percent = int(self.score / self.question_no * 100)
        return (self.score, wrong, score_percent)






#class "Quiz_Tkinter_Interface"
class Quiz_Tkinter_Interface:
    def __init__(self, quiz_brain):
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Trivia App")
        self.window.geometry("650x530")

        self.display_title()

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
        self.canvas.pack(pady=70)
        self.display_question()

        self.user_answer = StringVar()

        self.opts = self.radio_buttons()
        self.display_options()

        self.feedback = Label(self.window, pady=5, font=("Arial", 15, "bold"))
        #placement of the label
        self.feedback.place(x=90, y=380)

        #Next and Quit Button
        self.buttons()

        #Mainloop
        self.window.mainloop()


    #To display title
    def display_title(self):

        title = Label(self.window, text="Trivia Application",
                      width=30, bg=THEME_COLOR, fg="white", font=("Arial", 30, "bold"))

        title.place(x=0, y=2)

    #To display the question
    def display_question(self):
        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    #To create four options (radio buttons)
    def radio_buttons(self):
        

        choice_list = []

        #position of the first option
        y_pos = 220

        #Adding the options to the list
        while len(choice_list) < 4:

            radio_btn =Radiobutton(self.window, text="", variable=self.user_answer,
                                    value='', font=("Arial", 14))
            


            #adding the button to the list
            choice_list.append(radio_btn)

            # placing the button
            radio_btn.place(x=100, y=y_pos)

            y_pos += 40

        #return the radio buttons
        return choice_list

    #To display four options
    def display_options(self):

        val = 0

        self.user_answer.set(None)

        for option in self.quiz.current_question.choices:
            self.opts[val]['text'] = option
            self.opts[val]['value'] = option
            val += 1

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
            self.display_question()
            self.display_options()
        else:
            self.display_result()

            self.window.destroy()

    def buttons(self):

        next_button =ctk.CTkButton(self.window, text="Next", command=self.next_btn,
                             width=100,height=10, hover_color=THEME_COLOR,fg_color="green", font=("Arial", 20, "bold"))

        next_button.place(x=70, y=460)

        quit_button =ctk.CTkButton(self.window, text="Quit", command=self.window.destroy,
                             width=100,height=10, hover_color=THEME_COLOR,fg_color="red", corner_radius=5, font=("Arial", 20, "bold"))

        quit_button.place(x=500, y=460)

    def display_result(self):
        
        correct, wrong, score_percent = self.quiz.get_score()

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        result = f"Score: {score_percent}%"

        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")


#for loop
question_bank_list = []
for question in var_response_question_data:
    choices = []
    question_text = html.unescape(question["question"]) 
    correct_answer = html.unescape(question["correct_answer"])
    incorrect_answers = question["incorrect_answers"]
    for ans in incorrect_answers:
        choices.append(html.unescape(ans))
    choices.append(correct_answer)
    
    new_question = Question(question_text, correct_answer, choices)
    question_bank_list.append(new_question)


quiz = Quiz_operation(question_bank_list)

quiz_ui = Quiz_Tkinter_Interface(quiz)

print("You've completed the quiz")
print(f"Your final score was: {quiz.score}/{quiz.question_no}")
