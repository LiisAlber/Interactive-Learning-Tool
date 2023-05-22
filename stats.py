import os

class StatisticsMode:
    def __init__(self, question_manager):
        self.question_manager = question_manager



    def statistics_view(self):
        """
        Displays the statistics of each question.
        """
        print("\n--- Statistics Viewing Mode ---")
        print("ID | Active | Question Text | Shown | Correct | Correct %")
        print("------------------------------------------------------------")
        for question in self.question_manager.questions:
            active_status = "Yes" if question.enabled else "No"
            question_text = question.question_text
            shown_count = question.shown_count
            correct_count = question.correct_count
            correct_percentage = question.get_correct_percentage()

            print(f"{question.question_id} | {active_status} | {question_text} | {shown_count} | {correct_count} | {correct_percentage:.2f}%")


    def get_shown_count(self, question_id):
        """
        Returns the total shown count of a question.
        """
        total_count = 0
        for question in self.question_manager.questions:
            if question.question_id == question_id:
                total_count += question.weight
        return total_count
    

    def calculate_correct_percentage(self, shown_count, correct_count):
        """
        Calculates the correct percentage based on the shown count and correct count.
        """
        if shown_count == 0:
            return 0.0
        return (correct_count / shown_count) * 100
    

    def load_statistics(self):
        """
        Loads the statistics from the statistics file and updates the corresponding questions.
        """
        statistics_file_path = "statistics.txt"
        if os.path.isfile(statistics_file_path):
            with open(statistics_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    statistics_data = line.strip().split('|')
                    question_id = int(statistics_data[0])
                    enabled = statistics_data[1] == 'True'
                    question_text = statistics_data[2]
                    shown_count = int(statistics_data[3])
                    correct_count = int(statistics_data[4]) if statistics_data[4] else 0
                    # Compute the percentage of correct answers
                    correct_percentage = (correct_count / shown_count) * 100 if shown_count > 0 else 0

                    # Find the corresponding question and update the statistics
                    for question in self.question_manager.questions:
                        if question.question_id == question_id:
                            question.enabled = enabled
                            question.question_text = question_text
                            question.shown_count = shown_count
                            question.correct_count = correct_count
                            question.correct_percentage = correct_percentage
                            break


    def save_statistics(self):
        """
        Saves the statistics of each question to the statistics file.
        """
        statistics_file_path = "statistics.txt"
        with open(statistics_file_path, 'w') as file:
            for question in self.question_manager.questions:
                # Calculate the correct percentage and round it
                correct_percentage = self.calculate_correct_percentage(question.shown_count, question.correct_count)
                correct_percentage = round(correct_percentage, 2)
                
                question_data = [
                    question.question_id,
                    'True' if question.enabled else 'False',
                    question.question_text,
                    question.shown_count,
                    question.correct_count,
                    correct_percentage  # Add the rounded correct percentage to the data
                ]
                file.write('|'.join(str(data) for data in question_data) + '\n')


