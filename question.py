import re
import os
import random


class Question:
    next_id = 1
    
    def __init__(self, is_quiz=False):
        self.question_id = Question.next_id
        Question.next_id += 1
        self.is_quiz = is_quiz
        self.question_text = ""
        self.answer = ""
        self.answer_options = []
        self.enabled = True
        self.weight = 1
        self.expected_answer = ""
        self.shown_count = 0
        self.correct_count = 0
        self.correct_option_index = None


    def is_free_form(self):
        """
        Check if the question is a free-form question.
        """
        return not self.is_quiz
    

    def set_question_text(self, question_text):
        """
        Set the question text.
        """
        if not question_text:
            raise ValueError("Question text cannot be empty.")
        self.question_text = question_text


    def set_answer(self, answer):
        """
        Set the answer to the question.
        """
        if not answer:
            raise ValueError("Answer cannot be empty.")
        self.answer = answer


    def add_option(self, option, is_correct=False):
        """
        Add an option to a quiz question.
        """
        if self.is_quiz:
            self.answer_options.append(option)
            if is_correct:
                self.correct_option_index = len(self.answer_options) - 1
                self.answer = option


    def get_correct_percentage(self):
        """
        Calculate the percentage of correct answers.
        """
        if self.shown_count == 0:
            return 0.0
        return (self.correct_count / self.shown_count) * 100


    def increment_shown_count(self):
        """Increment the count of times the question has been shown."""
        self.shown_count += 1


    def increment_correct_count(self):
        """Increment the count of correct answers to the question."""
        self.correct_count += 1


    def get_shown_count(self):
        """
        Get the count of times the question has been shown.
        """
        return self.shown_count


    def get_correct_option_index(self):
        """
        Get the index of the correct option for a quiz question.
        """
        if self.is_quiz:
            for index, option in enumerate(self.answer_options):
                if option.strip().lower() == self.answer.strip().lower():
                    return index
        return None


    def compare_answers(self, user_answer):
        """
        Compare the user's answer to the expected answer.
        """
        user_answer = user_answer.strip()
        expected_answer = self.answer.strip()

        if re.match(r'^\d+$', expected_answer):
            try:
                return int(user_answer) == int(expected_answer)
            except ValueError:
                return False
        else:
            return user_answer.lower() == expected_answer.lower()
        

    def __str__(self):
        """
        Convert the Question object to a string representation.
        """
        question_type = "QuizQuestion" if self.is_quiz else "FreeformQuestion"
        if self.is_quiz:
            options = ",".join(str(option) for option in self.answer_options)
            return f"{self.question_id}|{str(self.enabled)}|{self.question_text}|{options}|{self.answer}|{question_type}"
        else:
            return f"{self.question_id}|{str(self.enabled)}|{self.question_text}|{self.answer}|{question_type}"

########################################################################################################################

from practice_test import PracticeMode, TestMode
from stats import StatisticsMode


class QuestionManager:

    def __init__(self, file_path="questions.txt"):
        """
        Manages the questions in the system.
        """
        self.questions = []
        self.file_path = file_path
        #self.load_questions()
        self.assign_question_ids()
        self.weights = []
        self.update_probabilities()
        self.statistics_view = StatisticsMode(self)
        self.load_questions()
        self.statistics_view.load_statistics()


    def assign_question_ids(self):
        """
        Assigns question IDs based on the existing questions in the list.
        """
        if self.questions:
            max_id = max(question.question_id for question in self.questions)
            Question.next_id = max_id + 1


    def update_probabilities(self):
        """
        Updates the probabilities for each question based on their weights.
        """
        self.probabilities = [question.weight for question in self.questions]


    def add_question_from_input(self):
        """
        Adds a question to the list based on user input.

        The user is prompted to select the type of question (free-form or quiz) and provide the necessary details.
        The question is then added to the list of questions.
        """
        while True:
            print("--- Add Question ---")
            print("Select the type of question:")
            print("1. Free-form Question")
            print("2. Quiz Question")
            print("3. Back to Main Menu")
            choice = input("Enter your choice (1, 2, or 3): ")

            if choice == "1":
                question_text = input("Enter the question text: ")
                answer = input("Enter the correct answer: ")
                if not re.match(r'^.+$', answer):
                    print("Invalid answer format. The answer should not be empty.")
                    continue
                question = Question(is_quiz=False)
                question.set_question_text(question_text)
                question.set_answer(answer)
                self.add_question_to_list(question)
                print("Question added successfully.")

            elif choice == "2":
                question_text = input("Enter the question text: ")
                option1 = input("Enter option 1: ")
                option2 = input("Enter option 2: ")
                option3 = input("Enter option 3: ")

                while True:
                    correct_answer_index = input("Enter the index of the correct answer (1, 2, or 3): ")
                    if correct_answer_index not in ["1", "2", "3"]:
                        print("Invalid correct answer index. Please choose 1, 2, or 3.")
                    else:
                        break

                question = Question(is_quiz=True)
                question.set_question_text(question_text)
                question.add_option(option1, is_correct=correct_answer_index=="1")
                question.add_option(option2, is_correct=correct_answer_index=="2")
                question.add_option(option3, is_correct=correct_answer_index=="3")
                

                self.add_question_to_list(question)
                print("Question added successfully.")


            elif choice == "3":
                break

            else:
                print("Invalid choice. Please try again.")


    def get_random_question(self):
        """
        Returns a random question from the list based on the weights.
        """
        if not self.questions:
            print("No questions available.")
            return None
        # Calculate total weight
        total_weight = sum(question.weight for question in self.questions)

        # Calculate weights for random.choice
        weights = [question.weight / total_weight for question in self.questions]

        # Select a random question based on weights
        selected_question = random.choices(self.questions, weights=weights)[0]

        return selected_question


    def add_question_to_list(self, question):
        """
        Adds a question to the list.
        """
        if not self.questions:
            question.question_id = 1
        else:
            question.question_id = self.questions[-1].question_id + 1
        self.questions.append(question)
        self.save_questions()


    def load_questions(self):
        """
        Loads questions from the file and adds them to the list.
        """
        self.questions = []  # Clear the existing questions
        if os.path.isfile(self.file_path):
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    question_data = line.strip().split('|')
                    question_id = int(question_data[0])
                    is_quiz = question_data[-1] == 'QuizQuestion'
                    question = Question(is_quiz)
                    question.question_id = question_id
                    question.enabled = question_data[1] == 'True'
                    question.question_text = question_data[2]
                    if is_quiz:
                        question.answer = question_data[-2]
                        question.answer_options = question_data[3].split(',')
                    else:
                        question.answer = question_data[3]
                    self.questions.append(question)
        self.assign_question_ids()


    def save_questions(self):
        """
        Saves the questions to the file.
        """
        with open(self.file_path, 'w') as file:
            for question in self.questions:
                file.write(str(question) + '\n')
    

    def get_question_by_id(self, question_id):
        """
        Retrieves a question from the list based on its ID.
        """
        for question in self.questions:
            if question.question_id == question_id:
                return question
        return None
    

    def get_enabled_questions(self):
        """
        Retrieves a list of enabled questions.
        """
        return [question for question in self.questions if question.enabled]


    def toggle_question_status(self):
        """
        Toggles the status (enabled/disabled) of a question.
        """
        while True:
            question_id = input("Enter the ID of the question you want to disable/enable: ")
            if not question_id.isdigit():
                print("Invalid question ID. Please enter a valid integer.")
                continue
            question_id = int(question_id)
            question = self.get_question_by_id(question_id)
            if question:
                print("Question Details:")
                print(f"Question ID: {question.question_id}")
                print(f"Question Text: {question.question_text}")
                print(f"Current Status: {'Enabled' if question.enabled else 'Disabled'}")
                while True:
                    confirm = input("Are you sure you want to toggle the status of this question? (y/n): ")
                    if confirm.lower() == "y":
                        question.enabled = not question.enabled
                        self.save_questions()
                        print("Question status toggled successfully.")
                        break
                    elif confirm.lower() == "n":
                        print("Question status toggle canceled.")
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
            else:
                print(f"Question with ID {question_id} not found.")
            break


    def delete_all_questions(self):
        """
        Deletes all questions from the list.
        """
        while True:
            confirm = input("Are you sure you want to delete all questions? This action cannot be undone. (y/n): ")
            if confirm.lower() == "y":
                self.questions = []
                Question.next_id = 1
                self.reset_weights()  # Reset weights to 1 for all questions
                self.save_questions()
                self.update_probabilities()
                
                # Clear statistics file
                with open('statistics.txt', 'w') as statistics_file:
                    statistics_file.truncate(0)  # Delete all content of the file
                
                print("All questions have been deleted.")
                break
            elif confirm.lower() == "n":
                print("Deletion canceled. No questions were deleted.")
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


    def reset_weights(self):
        """
        Resets the weights of all questions to 1.
        """
        for question in self.questions:
            question.weight = 1


    def run(self):
        """
        Runs the main interactive loop of the program.
        """
        print("\nWelcome to the Interactive Learning Tool!\n")

        if os.path.isfile(self.file_path):
            self.load_questions()
            print("Questions loaded successfully.")

        practice_mode = PracticeMode(self)
        test_mode = TestMode(self)
        statistics_view = StatisticsMode(self)
        statistics_view.load_statistics()

        while True:
            print("\n--- Menu ---")
            print("1. Add Questions")
            print("2. Toggle Question Status")
            print("3. Delete All Questions")
            print("4. Practice Mode")
            print("5. Test Mode")
            print("6. Statistics Viewing Mode")
            print("7. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_question_from_input()
                self.save_questions()

            elif choice == "2":
                self.toggle_question_status()
                self.save_questions()

            elif choice == "3":
                self.delete_all_questions()
                self.save_questions()

            elif choice == "4":
                practice_mode.practice_mode()
                practice_mode = PracticeMode(self)

            elif choice == "5":
                test_mode.test_mode()
                test_mode = TestMode(self)

            elif choice == "6":
                statistics_view.statistics_view()

            elif choice == "7":
                break

            else:
                print("Invalid choice. Please try again.")

        self.statistics_view.save_statistics()

        print("\nGoodbye! Thank you for using the Interactive Learning Tool.\n")


    def main(self):
        if os.path.isfile("questions.txt"):
            self.load_questions()
            self.statistics_view.load_statistics()

        self.run()

        self.statistics_view.save_statistics()


if __name__ == "__main__":
    manager = QuestionManager()
    manager.main()
