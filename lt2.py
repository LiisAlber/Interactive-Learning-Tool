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
        self.times_shown_practice = 0
        self.times_correct_practice = 0
        self.times_shown_test = 0
        self.times_correct_test = 0


    def show_question(self):
        print(self.text)

    def check_answer(self, user_answer):
        return user_answer.lower() == self.answer.lower()

    def show_statistics(self):
        print(f"Question ID: {self.qid}")
        print(f"Active: {self.is_active}")
        print(f"Question Text: {self.text}")
        print(f"Times Shown (Practice): {self.times_shown_practice}")
        print(f"Times Correct (Practice): {self.times_correct_practice}")
        print(f"Percentage Correct (Practice): {self.get_percentage_correct(is_test_mode=False)}%")
        print(f"Times Shown (Test): {self.times_shown_test}")
        print(f"Times Correct (Test): {self.times_correct_test}")
        print(f"Percentage Correct (Test): {self.get_percentage_correct(is_test_mode=True)}%")


    def get_percentage_correct(self, is_test_mode):
        if is_test_mode:
            if self.times_shown_test == 0:
                return 0
            return round(self.times_correct_test / self.times_shown_test * 100, 2)
        else:
            if self.times_shown_practice == 0:
                return 0
            return round(self.times_correct_practice / self.times_shown_practice * 100, 2)

    
    def update_stats(self, is_correct, is_test_mode):
        if is_test_mode:
            self.times_shown_test += 1
            if is_correct:
                self.times_correct_test += 1
        else:
            self.times_shown_practice += 1
            if is_correct:
                self.times_correct_practice += 1
        self.times_shown = self.times_shown_test + self.times_shown_practice
        self.percent_correct = self.get_percentage_correct(is_test_mode)



########################################################################################################

#This is a subclass of Question that represents a question where the user is expected to enter a free-form answer.
class FreeFormQuestion(Question):
    next_qid = 1

    def __init__(self, qid, text, answer, is_active=True):
        super().__init__(qid, text, answer, is_active)
        FreeFormQuestion.next_qid += 1


    def show_question(self):
        print(self.text)

    def check_answer(self, user_answer):
        return user_answer.lower() == self.answer.lower()
    
    def update_stats(self, is_correct, is_test_mode):
        super().update_stats(is_correct, is_test_mode)
        self.times_correct_practice += is_correct and not is_test_mode
        self.times_correct_test += is_correct and is_test_mode

    def ask_freeform_question(self):
        self.show_question()
        user_answer = input("Enter your answer: ")
        if self.check_answer(user_answer):
            print("Correct!")
            self.update_stats(True, False)
        else:
            print(f"Incorrect. The correct answer is: {self.answer}")
            self.update_stats(False, False)
###############################################################################################################

#This is another subclass of Question that represents a multiple-choice 
#question where the user is presented with a set of options to choose from.
class QuizQuestion(Question):
    next_qid = 1

    def __init__(self, qid, text, answer, options, is_active=True):
        super().__init__(qid, text, answer, is_active)
        self.options = options
        self.times_correct_practice = 0
        self.times_shown_practice = 0
        self.times_correct_test = 0
        self.times_shown_test = 0
        QuizQuestion.next_qid += 1

    
    def show_question(self):
        print(self.text)
        for i, option in enumerate(self.options):
            print(f"{i+1}. {option}")
    
    def check_answer(self, user_answer):
        return user_answer.lower() == self.answer.lower()
            
    def update_stats(self, is_correct, is_test_mode):
        super().update_stats(is_correct, is_test_mode)
        self.times_correct_practice += is_correct and not is_test_mode
        self.times_correct_test += is_correct and is_test_mode
        
    def ask_quiz_question(self):
        self.show_question()
        user_answer = input("Enter the correct option number: ")
        if self.check_answer(user_answer):
            print("Correct!")
            self.update_stats(True, False)
        else:
            print(f"Incorrect. The correct answer is: {self.answer}")
            self.update_stats(False, False)

##############################################################################################################################

#This class would be responsible for keeping track of the statistics for each question, 
#such as the number of times it was shown during practice or tests, and the percentage of times it was answered correctly.
class Statistics:
    def __init__(self, questions):
        self.questions = questions
        self.stats = {}
        self.disabled_questions = []

    def update_stats(self, question, correct):
        if question.qid not in self.stats:
            self.stats[question.qid] = {"times_shown": 0, "times_correct": 0}
        self.stats[question.qid]["times_shown"] += 1
        if correct:
            self.stats[question.qid]["times_correct"] += 1

    def get_statistics(self):
        for question in self.questions:
            if question.is_active:
                num_shown_practice = question.times_shown_practice
                percent_correct_practice = question.get_percentage_correct(is_test_mode=False)
                num_shown_test = question.times_shown_test
                percent_correct_test = question.get_percentage_correct(is_test_mode=True)
                print(f"ID: {question.qid} | Active: {question.is_active} | Text: {question.text}")
                print(f"Times shown (Practice): {num_shown_practice} | Percent correct (Practice): {percent_correct_practice:.2f}%")
                print(f"Times shown (Test): {num_shown_test} | Percent correct (Test): {percent_correct_test:.2f}%\n")

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
        self.statistics = Statistics(self.questions)

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
                self.statistics.get_statistics()
            elif choice == "3":
                self.toggle_question_active_status()
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
            qid = QuizQuestion.next_qid
            question = QuizQuestion(qid, text, answer, options)
            QuizQuestion.next_qid += 1
            save_question_to_file(question)
            print("Quiz question added successfully.")
        elif question_type == "2":
            text = input("Enter question: ")
            answer = input("Enter answer: ")
            qid = FreeFormQuestion.next_qid
            question = FreeFormQuestion(qid, text, answer)
            FreeFormQuestion.next_qid += 1
            save_question_to_file(question)
            print("Free-form question added successfully.")
        else:
            print("Invalid choice.")

        QuizQuestion.next_qid += 1
        FreeFormQuestion.next_qid += 1

        self.save_questions()

    def get_statistics(self):
        self.stats.get_statistics()
        
    def toggle_question_active_status(self):
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
        
        random.shuffle(quiz_questions)
        random.shuffle(freeform_questions)
        
        quiz_question_count = min(num_questions // 2, len(quiz_questions))
        freeform_question_count = num_questions - quiz_question_count
        
        selected_questions = quiz_questions[:quiz_question_count] + freeform_questions[:freeform_question_count]
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
        with open("questions.txt", "r") as f:
            for line in f:
                question_data = line.strip().split("|")
                if question_data[0] == "QuizQuestion":
                    qid, text, answer, is_active, options = question_data[1:]
                    options = options.split(",")
                    q = QuizQuestion(int(qid), text, answer, options, is_active=="True")
                elif question_data[0] == "FreeFormQuestion":
                    qid, text, answer, is_active = question_data[1:]
                    q = FreeFormQuestion(int(qid), text, answer, is_active=="True")
                else:
                    continue
                self.questions.append(q)


    def load_disabled_questions(self):
        try:
            with open("disabled_questions.txt", "r") as f:
                data = f.readlines()
            for line in data:
                qid = int(line.strip())
                if qid not in self.disabled_questions:
                    self.disabled_questions.append(qid)
        except FileNotFoundError:
            return


    def get_question_by_id(self, qid):
        for question in self.questions:
            if question.qid == qid:
                return question
        return None

    def disable_question(self, qid):
        question = self.get_question_by_id(qid)
        if question is None:
            print("Error: Invalid question ID.")
            return False
        if qid in self.disabled_questions:
            print("Error: Question is already disabled.")
            return False
        question.is_active = False
        self.disabled_questions.append(qid)
        self.save_disabled_questions()
        return True

    def enable_question(self, qid):
        question = self.get_question_by_id(qid)
        if question is None:
            print("Error: Invalid question ID.")
            return False
        if qid not in self.disabled_questions:
            print("Error: Question is already enabled.")
            return False
        question.is_active = True
        self.disabled_questions.remove(qid)
        self.save_disabled_questions()
        return True
    
    def save_questions(self):
        with open("questions.txt", "a") as f:
            for question in self.questions:
                if isinstance(question, QuizQuestion):
                    options_str = ",".join([str(option) for option in question.options])
                    line = f"QuizQuestion|{question.qid}|{question.text}|{question.answer}|{question.is_active}|{options_str}\n"
                elif isinstance(question, FreeFormQuestion):
                    line = f"FreeFormQuestion|{question.qid}|{question.text}|{question.answer}|{question.is_active}\n"
                f.write(line)

    def save_question_to_file(questions):
        with open("questions.txt", "w") as f:
            for question in questions:
                if isinstance(question, QuizQuestion):
                    options_str = ",".join([str(option) for option in question.options])
                    line = f"QuizQuestion|{question.qid}|{question.text}|{question.answer}|{question.is_active}|{options_str}\n"
                elif isinstance(question, FreeFormQuestion):
                    line = f"FreeFormQuestion|{question.qid}|{question.text}|{question.answer}|{question.is_active}\n"
                f.write(line)


    def save_disabled_questions(self):
        with open("disabled_questions.txt", "w") as f:
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
        total_weight = sum(weights)
        threshold = random.uniform(0, total_weight)
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