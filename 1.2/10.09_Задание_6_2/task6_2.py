import tkinter as tk
from tkinter import Radiobutton


class TestApp(tk.Tk):
    def __init__(self, questions):
        super().__init__()
        self.title("Тестовая система")
        self.geometry("400x300")
        
        self.questions = questions
        self.current_question = 0
        self.correct_answers = 0
        
        self.question_label = tk.Label(self, text="")
        self.question_label.pack()
        
        self.selected_answer = tk.IntVar()
        self.answer_radios = []

        #Примем кол-во ответов равное 4 (ни больше, ни меньше)
        for i in range(4):
            radio = Radiobutton(self, text="", variable=self.selected_answer, value=i)
            radio.pack()
            self.answer_radios.append(radio)
        
        self.check_button = tk.Button(self, text="Ответить", command=self.check_answer)
        self.check_button.pack()
        
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.result_label_percent = tk.Label(self, text="")
        self.result_label_percent.pack()

        self.load_questions()
        self.display_question()
        
    def load_questions(self):
        with open("questions.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            question = None
            for line in lines:
                line = line.strip()
                if line.startswith("q:"):
                    if question:
                        self.questions.append(question)
                    question = {"q": line[3:], "a": []}
                elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
                    is_correct = line.endswith("+")
                    if is_correct:
                        answer = line[3:-1]
                    else:
                        answer = line[3:]
                    question["a"].append({"answer": answer, "correct": is_correct})
        
        # Добавляем последний вопрос
        if question:
            self.questions.append(question)
    
    def display_question(self):
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label.configure(text=question["q"])
            
            for i, answer_obj in enumerate(question["a"]):
                radio = self.answer_radios[i]
                radio.configure(text=answer_obj["answer"])
                
            self.check_button.configure(state=tk.NORMAL)
        else:
            self.check_button.configure(state=tk.DISABLED)
            self.show_result()
    
    def check_answer(self):
        question = self.questions[self.current_question]
        answer_obj = question["a"][self.selected_answer.get()]
        
        if answer_obj["correct"]:
            self.correct_answers += 1
        
        self.current_question += 1
        self.display_question()
    
    def show_result(self):
        total_questions = len(self.questions)
        percentage = (self.correct_answers / total_questions) * 100
        
        self.result_label.configure(text=f"Количество правильных ответов: {self.correct_answers}/{total_questions}")
        self.result_label_percent.configure(text=f"Процент правильных ответов: {percentage:.2f}%")


if __name__ == "__main__":
    questions = []
    
    app = TestApp(questions)
    app.mainloop()