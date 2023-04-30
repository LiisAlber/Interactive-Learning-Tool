import random
import re
import os
print(os.getcwd())


class Question:
    def __init__(self, qid, text, answer, is_active=True):
        self.qid = qid
        self.text = text
        self.answer = answer
        self.is_active = is_active
        self.times_shown = 0
        self.times_correct = 0

    def __str__(self):
        return f"{self.qid}. {self.text}\nActive: {self.is_active}\nTimes shown: {self.times_shown}\nTimes answered correctly: {self.times_correct} ({self.get_percentage_correct()}%)\n"

    def get_percentage_correct(self):
        if self.times_shown == 0:
            return 0
        return round(self.times_correct / self.times_shown * 100, 2)

    def is_correct(self, user_answer):
        if not super().is_correct(user_answer):
            return False
        for option in self.options:
            pattern = re.compile(rf"\b{option}\b", re.IGNORECASE)
            if pattern.search(user_answer):
                return True
        return False

    def disable(self):
        self.is_active = False

    def enable(self):
        self.is_active = True

########################################################################################################

class QuizQuestion(Question):
    def __init__(self, qid, text, answer, options, is_active=True):
        super().__init__(qid, text, answer, is_active)
        self.options = options

    def __str__(self):
        return super().__str__() + f"Options: {', '.join(self.options)}\n"

    def is_valid_option(self, user_answer):
        return user_answer in self.options

#########################################################################################################

class LearningTool:
    def __init__(self):
        self.questions = []
        self.disabled_questions = set()
        self.load_questions()

    def run(self):
        print("Welcome to the Learning Tool!")
        while True:
            print("Select mode:")
            print("1. Add questions")
            print("2. View statistics")
            print("3. Disable/Enable questions")
            print("4. Practice mode")
            print("5. Test mode")
            choice = input("> ")
            if choice == "1":
                self.add_questions_mode()
            elif choice == "2":
                self.statistics_viewing_mode()
            elif choice == "3":
                self.disable_enable_questions_mode()
            elif choice == "4":
                self.practice_mode()
            elif choice == "5":
                self.test_mode()
            else:
                print("Invalid choice, please try again")

    def add_questions_mode(self):
        print("Select question type:")
        print("1. Quiz question")
        print("2. Free-form text question")
        qtype = input("> ")
        if qtype == "1":
            text = input("Enter question text: ")
            answer = input("Enter correct answer: ")
            options = []
            while True:
                option = input("Enter option (or leave blank to finish): ")
                if option:
                    options.append(option)
                else:
                    break
            qid = len(self.questions) + 1
            self.questions.append(QuizQuestion(qid, text, answer, options))
            print("Question added!")
        elif qtype == "2":
            text = input("Enter question text: ")
            answer = input("Enter correct answer: ")
            qid = len(self.questions) + 1
            self.questions.append(Question(qid, text, answer))
            print("Question added!")
        else:
            print("Invalid choice, please try again")

        self.save_questions()

    def statistics_viewing_mode(self):
        if not self.questions:
            print("No questions added yet!")
            return

        print("Question statistics:")
        for question in self.questions:
            print(question)

    def disable_enable_questions_mode(self):
        self.print_questions()
        question_id = input("Enter the ID of the question you want to disable/enable: ")
        question = self.question_bank.get_question_by_id(question_id)
        if question:
            print("Question found: ")
            self.print_question(question)
            action = input("Do you want to disable or enable this question? (d/e): ")
            if action == "d":
                question.disable()
            elif action == "e":
                question.enable()
            self.question_bank.save_questions()
            print("Question status updated.")
        else:
            print("Question not found.")

    '''def save_questions(self):
        with open("questions.txt", "w") as file:
            for question in self.questions:
                qtype = "quiz" if isinstance(question, QuizQuestion) else "freeform"
                options = ",".join(question.options) if isinstance(question, QuizQuestion) else ""
                line = f"{qtype},{question.qid},{question.text},{question.answer},{options},{question.is_active}\n"
                file.write(line)'''

    '''def disable_enable_questions_mode(self):
        question_id = input("Enter the ID of the question you want to disable/enable: ")
        question = self.get_question_by_id(question_id)
        if question:
            print("Question found: ")
            print(question)
            action = input("Do you want to disable or enable this question? (d/e): ")
            if action == "d":
                question.disable()
            elif action == "e":
                question.enable()
            self.save_questions()
            print("Question status updated.")
        else:
            print("Question not found.")'''


    def load_questions(self):
        try:
            with open("questions.txt", "r") as file:
                for line in file:
                    fields = line.strip().split(",")
                    qtype = fields[0]
                    qid = int(fields[1])
                    text = fields[2]
                    answer = fields[3]
                    options = fields[4].split(";") if fields[4] else []
                    is_active = fields[5] == "True"
                    if qtype == "QuizQuestion":
                        self.questions.append(QuizQuestion(qid, text, answer, options, is_active))
                    elif qtype == "Question":
                        self.questions.append(Question(qid, text, answer, is_active))
        except FileNotFoundError:
            pass


    def save_questions(self):
        with open("questions.txt", "w") as file:
            for question in self.questions:
                if isinstance(question, QuizQuestion):
                    qtype = "QuizQuestion"
                    options = ";".join(question.options)
                else:
                    qtype = "Question"
                    options = ""
                line = f"{qtype},{question.qid},{question.text},{question.answer},{options},{question.is_active}\n"
                file.write(line)

######################################################################################################################

class QuestionBank:
    def __init__(self):
        self.questions = []
        self.disabled_questions = []

    def add_question(self, question):
        self.questions.append(question)

    def get_question_by_id(self, question_id):
        for question in self.questions:
            if question.id == question_id:
                return question
        return None

    def get_questions(self, is_disabled=False):
        if is_disabled:
            return self.disabled_questions
        return [q for q in self.questions if q not in self.disabled_questions]

    def disable_question(self, question_id):
        question = self.get_question_by_id(question_id)
        if question:
            self.disabled_questions.append(question)
            self.questions.remove(question)

    def enable_question(self, question_id):
        question = self.get_question_by_id(question_id)
        if question and question in self.disabled_questions:
            self.questions.append(question)
            self.disabled_questions.remove(question)
            
###################################################################################################################

if __name__ == '__main__':
    tool = LearningTool()
    tool.run()

       
