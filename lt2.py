import random
import datetime
import re
import os

#This would be a base class that all other question types inherit from. 
#It could have properties such as text, answer, is_active, etc.
class Question:
    def __init__(self, qid, text, answer, is_active=True):
        self.qid = qid
        self.text = text
        self.answer = answer
        self.is_active = is_active
        self.times_shown = 0
        self.times_correct = 0
        self.times_incorrect = 0

    def show_question(self):
        print(self.text)

    def check_answer(self, user_answer):
        is_correct = user_answer.strip().lower() == self.answer.strip().lower()
        if is_correct:
            self.times_correct += 1
        else:
            self.times_incorrect += 1
        self.times_shown += 1
        return is_correct

    def show_statistics(self):
        print(f"Question ID: {self.qid}")
        print(f"Active: {self.is_active}")
        print(f"Question Text: {self.text}")
        print(f"Times Shown: {self.times_shown}")
        print(f"Times Correct: {self.times_correct}")
        print(f"Percentage Correct: {self.get_percentage_correct()}%")

    def get_percentage_correct(self):
        if self.times_shown == 0:
            return 0
        return round(self.times_correct / self.times_shown * 100, 2)

########################################################################################################

#This is a subclass of Question that represents a question where the user is expected to enter a free-form answer.
class FreeFormQuestion(Question):
    def __init__(self, qid, text, answer, is_active=True):
        super().__init__(qid, text, answer, is_active)

    def show_question(self):
        print(self.text)

    def check_answer(self, user_answer):
        return user_answer.strip().lower() == self.answer.strip().lower()
    
    def update_stats(self, is_correct):
        if is_correct:
            self.times_correct += 1
        else:
            self.times_incorrect += 1

    def ask_freeform_question(self):
        self.show_question()
        user_answer = input("Enter your answer: ")
        if self.check_answer(user_answer):
            print("Correct!")
            self.times_correct += 1
        else:
            print(f"Incorrect. The correct answer is: {self.answer}")
            self.times_incorrect += 1
    
###############################################################################################################

#This is another subclass of Question that represents a multiple-choice 
#question where the user is presented with a set of options to choose from.
class QuizQuestion(Question):
    def __init__(self, qid, text, answer, options, is_active=True):
        super().__init__(qid, text, answer, is_active)
        self.options = options
        self.times_correct = 0
        self.times_incorrect = 0
    
    def show_question(self):
        print(self.text)
        for i, option in enumerate(self.options):
            print(f"{i+1}. {option}")
    
    def check_answer(self, user_answer):
        if isinstance(self, Question):
            return user_answer.strip().lower() == self.answer.strip().lower()
        elif isinstance(self, QuizQuestion):
            if user_answer.isdigit() and int(user_answer) <= len(self.options):
                return self.options[int(user_answer) - 1].strip().lower() == self.answer.strip().lower()
            else:
                return False
            
    def update_stats(self, is_correct):
        if is_correct:
            self.times_correct += 1
        else:
            self.times_incorrect += 1

    
        
    def ask_quiz_question(self):
        self.show_question()
        user_answer = input("Enter the correct option number: ")
        if self.check_answer(user_answer):
            print("Correct!")
            self.times_correct += 1
        else:
            print(f"Incorrect. The correct answer is: {self.answer}")
            self.times_incorrect += 1

##############################################################################################################################

#This class would be responsible for keeping track of the statistics for each question, 
#such as the number of times it was shown during practice or tests, and the percentage of times it was answered correctly.
class Statistics:
    def __init__(self, questions):
        self.questions = questions
        self.stats = {}

    def update_stats(self, question, correct):
        if question.qid not in self.stats:
            self.stats[question.qid] = {"times_shown": 0, "times_correct": 0}
        self.stats[question.qid]["times_shown"] += 1
        if correct:
            self.stats[question.qid]["times_correct"] += 1

    def get_statistics(self):
        for question in self.questions:
            num_shown = question.times_correct + question.times_incorrect
            if num_shown > 0:
                percent_correct = (question.times_correct / num_shown) * 100
            else:
                percent_correct = 0
            print(f"ID: {question.qid} | Active: {question.is_active} | Text: {question.text}")
            print(f"Times shown: {num_shown} | Percent correct: {percent_correct:.2f}%\n")

###########################################################################################################################

#This is the main class that ties everything together. 
# It would have methods for adding questions, viewing statistics, disabling/enabling questions, practicing, testing, 
# and any other functionality you decide to implement.
class LearningTool: 
    def __init__(self):
        self.questions = []
        self.load_questions()
        self.disabled_questions = []
        self.load_disabled_questions()
        self.practice_question_count = 0

    def run(self):
        print("Welcome to the Learning Tool!")
        while True:
            print("\nWhat would you like to do?")
            print("1. Add a new question")
            print("2. View question statistics")
            print("3. Disable or enable a question")
            print("4. Enter practice mode")
            print("5. Enter test mode")
            print("6. Exit program")
            choice = input("Enter choice: ")
            if choice == "1":
                self.add_question()
            elif choice == "2":
                self.view_statistics()
            elif choice == "3":
                self.disable_enable_questions()
            elif choice == "4":
                self.practice_mode()
            elif choice == "5":
                self.test_mode()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")

        self.save_questions()
        self.save_disabled_questions()


    def add_question(self):
        print("What type of question would you like to add?")
        print("1. Quiz question")
        print("2. Free-form question")
        question_type = input("Enter choice: ")
        if question_type == "1":
            text = input("Enter question: ")
            options = []
            while True:
                option = input("Enter option (or 'd' to finish): ")
                if option == "d":
                    break
                options.append(option)
            answer = input("Enter answer: ")
            self.questions.append(QuizQuestion(len(self.questions) + 1, text, answer, options))
            print("Quiz question added successfully.")
        elif question_type == "2":
            text = input("Enter question: ")
            answer = input("Enter answer: ")
            self.questions.append(FreeFormQuestion(len(self.questions) + 1, text, answer))
            print("Free-form question added successfully.")
        else:
            print("Invalid choice.")

        self.save_questions()


    def view_statistics(self):
        self.stats.get_statistics()

    def disable_enable_questions(self):
        print("Which question would you like to disable/enable?")
        question_id = int(input("Enter question ID: "))
        question = self.get_question_by_id(question_id)
        if question is None:
            print("Invalid question ID.")
            return
        print(f"Question ID: {question_id}")
        print(f"Question text: {question.text}")
        action = input("Do you want to disable or enable this question? (d/e): ")
        if action == "d":
            self.disable_question(question_id)
            print("Question disabled.")
        elif action == "e":
            self.enable_question(question_id)
            print("Question enabled.")
        else:
            print("Invalid choice.")

        self.save_questions()
        self.save_disabled_questions()


    def practice_mode(self):
        active_questions = self.get_active_questions()
        if not active_questions:
            print("There are no active questions to practice. Exiting practice mode.")
            return
        
        while True:
            question = self.weighted_choice(active_questions)
            print(question.text)
            user_answer = input("Enter your answer (or 'q' to quit): ")
            if user_answer == "q":
                break
            
            is_correct = question.check_answer(user_answer)
            if is_correct:
                question.times_correct += 1
                print("Correct!")
            else:
                question.times_incorrect += 1
                print("Incorrect!")

            question.update_stats(is_correct)
            self.save_questions()
    
    def weighted_choice(self, choices):
        weights = [q.times_incorrect + 1 for q in choices]
        total_weight = sum(weights)
        rand_num = random.uniform(0, total_weight)
        weight_sum = 0
        for i, choice in enumerate(choices):
            weight_sum += weights[i]
            if rand_num <= weight_sum:
                return choice

    def test_mode(self):
        active_questions = self.get_active_questions()
        if len(active_questions) < 5:
            print("There are not enough active questions to enter Test mode.")
            return
        
        quiz_questions = []
        freeform_questions = []
        for question in active_questions:
            if isinstance(question, QuizQuestion):
                quiz_questions.append(question)
            elif isinstance(question, FreeFormQuestion):
                freeform_questions.append(question)
            
        num_questions = input("Enter the number of questions for the test: ")
        while not num_questions.isdigit() or int(num_questions) > len(active_questions):
            num_questions = input(f"Please enter a valid number of questions (1 - {len(active_questions)}): ")
        num_questions = int(num_questions)
        
        quiz_question_count = min(num_questions // 2, len(quiz_questions))
        freeform_question_count = num_questions - quiz_question_count
        
        quiz_questions = random.sample(quiz_questions, quiz_question_count)
        freeform_questions = random.sample(freeform_questions, freeform_question_count)
        
        selected_questions = quiz_questions + freeform_questions
        random.shuffle(selected_questions)
        
        score = 0
        print("Test mode started!")
        for question in selected_questions:
            print(f"Question {selected_questions.index(question) + 1}: {question.text}")
            if isinstance(question, QuizQuestion):
                print("Options:")
                for option in question.options:
                    print(option)
                while True:
                    answer = input("Choose the correct option: ")
                    if answer.isdigit() and int(answer) in range(1, len(question.options)+1):
                        if question.options[int(answer) - 1] == question.answer:
                            print("Correct!")
                            score += 1
                            question.update_stats(True)
                        else:
                            print(f"Incorrect. The correct answer is: {question.answer}")
                            question.update_stats(False)
                        break
                    else:
                        print(f"Please enter a valid option number (1 - {len(question.options)}):")
            else:
                answer = input("Enter your answer: ")
                if answer.lower() == question.answer.lower():
                    print("Correct!")
                    score += 1
                    question.update_stats(True)
                else:
                    print(f"Incorrect. The correct answer is: {question.answer}")
                    question.update_stats(False)

        score_percentage = (score / num_questions) * 100
        print(f"\nTest finished. Your score: {score}/{num_questions} ({score_percentage:.2f}%).")
        self.save_test_result(score_percentage)

        
    def load_questions(self):
        try:
            with open("questions2.txt", "r") as f:
                data = f.readlines()
        except FileNotFoundError:
            with open("questions2.txt", "w") as f:
                print("Created new questions2.txt file.")
            return
            
        for i, line in enumerate(data):
            line = line.strip()
            if line.startswith("QuizQuestion"):
                fields = line.split("|")
                if len(fields) == 5:
                    qid, text, answer, is_active, options_str = fields
                    options = options_str.split(",")
                    self.questions.append(QuizQuestion(int(qid), text, answer, options, is_active == "True"))
                else:
                    print(f"Skipping line {i} in questions2.txt: {line}")
            elif line.startswith("FreeFormQuestion"):
                fields = line.split("|")
                if len(fields) == 4:
                    qid, text, answer, is_active = fields
                    self.questions.append(FreeFormQuestion(int(qid), text, answer, is_active == "True"))
                else:
                    print(f"Skipping line {i} in questions2.txt: {line}")
            else:
                print(f"Skipping line {i} in questions2.txt: {line}")

    def load_disabled_questions(self):
        try:
            with open("disabled_questions2.txt", "r") as f:
                data = f.readlines()
            for line in data:
                self.disabled_questions.append(int(line.strip()))
        except FileNotFoundError:
            with open("disabled_questions2.txt", "w") as f:
                pass
            return


    def get_question_by_id(self, qid):
        for question in self.questions:
            if question.qid == qid:
                return question
        return None

    def disable_question(self, qid):
        question = self.get_question_by_id(qid)
        if question is None:
            return False
        if qid in self.disabled_questions:
            return False
        question.is_active = False
        self.disabled_questions.append(qid)
        self.save_disabled_questions()
        return True

    def enable_question(self, qid):
        question = self.get_question_by_id(qid)
        if question is None:
            return False
        if qid not in self.disabled_questions:
            return False
        question.is_active = True
        self.disabled_questions.remove(qid)
        self.save_disabled_questions()
        return True
    
    def save_questions(self):
        with open("questions2.txt", "w") as f:
            for question in self.questions:
                if isinstance(question, QuizQuestion):
                    options_str = ",".join([str(option) for option in question.options])
                    line = f"QuizQuestion|{question.qid}|{question.text}|{question.answer}|{question.is_active}|{options_str}\n"
                elif isinstance(question, FreeFormQuestion):
                    line = f"FreeFormQuestion|{question.qid}|{question.text}|{question.answer}|{question.is_active}\n"
                f.write(line)

    def save_disabled_questions(self):
        with open("disabled_questions2.txt", "w") as f:
            for qid in self.disabled_questions:
                f.write(str(qid) + "\n")

    def get_active_questions(self):
        active_questions = []
        for question in self.questions:
            if question.is_active and question.qid not in self.disabled_questions:
                active_questions.append(question)
        return active_questions

    def weighted_choice(self, choices):
        weights = [q.times_incorrect + 1 for q in choices]
        total = sum(weights)
        threshold = random.uniform(0, total)
        for i, w in enumerate(weights):
            threshold -= w
            if threshold <= 0:

                return choices[i]
            
    def save_test_result(self, score_percentage):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        with open("results.txt", "a") as f:
            f.write(f"{timestamp} | Score: {score_percentage:.2f}%\n")

    

###############################################################################################

if __name__ == '__main__':
    tool = LearningTool()
    tool.run()