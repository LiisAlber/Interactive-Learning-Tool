import random
import datetime

class PracticeMode:

    def __init__(self, question_manager):
        self.question_manager = question_manager


    def get_random_question(self):
        """
        Retrieves a random enabled question for practice mode.
        """
        if len(self.question_manager.get_enabled_questions()) < 5:
            print("At least 5 active questions are required for practice mode.")
            return None

        # Calculate total weight
        total_weight = sum(question.weight for question in self.question_manager.get_enabled_questions())

        # Calculate weights for random.choices
        weights = [question.weight / total_weight for question in self.question_manager.get_enabled_questions()]

        # Select a random question based on weights
        selected_question = random.choices(self.question_manager.get_enabled_questions(), weights=weights)[0]

        return selected_question
    

    def practice_mode(self):
        """
        Runs the practice mode.
        """
        score = 0
        print("\n--- Practice Mode ---")

        while True:
            question = self.get_random_question()
            if question is None:
                break

            print(f"\nQuestion {question.question_id}: {question.question_text}")
            question.shown_count += 1

            if question.is_free_form():
                while True:
                    user_answer = input("Enter your answer or 'q' to quit: ")
                    if user_answer.lower() == 'q':
                        break
                    if user_answer.strip() == "":
                        print("Please enter a valid answer.")
                        continue
                    if question.compare_answers(user_answer):
                        print("Correct answer!")
                        question.increment_shown_count()
                        question.increment_correct_count()
                        question.correct_count += 1
                        question.weight *= 0.8  # decrease weight
                    else:
                        print(f"Incorrect answer! The correct answer is {question.answer}.")
                        question.weight *= 1.2  # increase weight
                    break
            else:
                while True:
                    for index, option in enumerate(question.answer_options):
                        print(f"{index + 1}. {option}")
                    user_answer = input("Enter the number of the correct option or 'q' to quit: ")
                    if user_answer.lower() == 'q':
                        break
                    if user_answer.strip() == "":
                        print("Please enter a valid option.")
                        continue
                    try:
                        user_option = int(user_answer) - 1
                        if user_option < 0 or user_option >= len(question.answer_options):
                            print("Please enter a valid option.")
                            continue
                        correct_option_index = question.get_correct_option_index()
                        if correct_option_index is not None and user_option == correct_option_index:
                            print("Correct answer!")
                            question.increment_shown_count()
                            question.increment_correct_count()
                            score += 1
                            question.correct_count += 1
                            question.weight *= 0.8  # decrease weight
                        else:
                            if correct_option_index is not None:  
                                print(f"Incorrect answer! The correct option is {correct_option_index + 1}.")
                            else:
                                print("Incorrect answer!")
                            question.increment_shown_count()
                            question.weight *= 1.2  # increase weight
                        break
                    except ValueError:
                        print("Please enter a valid option.")
                        continue


            self.question_manager.update_probabilities()
            self.question_manager.save_questions()

            if user_answer.lower() == 'q':
                break



class TestMode:
    def __init__(self, question_manager):
        self.question_manager = question_manager


    def test_mode(self):
        """
        Runs the test mode.
        """
        print("\n--- Test Mode ---")
        num_questions = int(input("Enter the number of questions for the test: "))

        if num_questions < 5:
            print("Minimum 5 questions are required to enter the test mode.")
            return

        questions = self.question_manager.get_enabled_questions()
        if len(questions) < num_questions:
            print(f"Insufficient number of questions available. Total questions: {len(questions)}")
            return

        selected_questions = random.sample(questions, num_questions)
        score = 0

        print("--- Test Started ---")
        question_number = 1
        for question in selected_questions:
            print(f"\nQuestion {question_number}: {question.question_text}")
            question_number += 1
            question.shown_count += 1

            if question.is_free_form():
                while True:
                    user_answer = input("Enter your answer: ")
                    if user_answer.strip() != "":
                        break
                    print("Please enter a valid answer.")
                if question.compare_answers(user_answer):
                    print("Correct answer!")
                    score += 1
                    question.correct_count += 1
                else:
                    print(f"Incorrect answer! The correct answer is {question.answer}.")
            else:
                for index, option in enumerate(question.answer_options):
                    print(f"{index + 1}. {option}")
                while True:
                    user_answer = input("Enter the number of the correct option: ")
                    try:
                        user_option = int(user_answer)
                        if user_option >= 1 and user_option <= len(question.answer_options):
                            correct_option_index = question.get_correct_option_index()
                            if correct_option_index is not None and user_option - 1 == correct_option_index:
                                print("Correct answer!")
                                score += 1
                                question.correct_count += 1
                            else:
                                if correct_option_index is not None:  
                                    print(f"Incorrect answer! The correct option is {correct_option_index + 1}.")
                                else:
                                    print("Incorrect answer!")
                            break
                        else:
                            print("Please enter a valid option.")
                    except ValueError:
                        print("Please enter a valid option.")

        print("\n--- Test Finished ---")
        percentage = (score / num_questions) * 100
        print(f"Score: {percentage:.2f}% | Questions: {score}/{num_questions}")

        self.record_result(percentage, score, num_questions)



    def record_result(self, score_percentage, num_correct, num_questions):
        """
        Records the test result to a file.
        """
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        result = f"{timestamp} | Score: {score_percentage:.2f}% | Questions: {num_correct}/{num_questions}\n"

        with open("results.txt", "a") as file:
            file.write(result)

   

        
