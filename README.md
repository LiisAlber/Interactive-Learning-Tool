# Interactive Learning Tool
The Interactive Learning Tool is a command-line program designed to facilitate interactive learning and testing with a collection of questions. It provides features for adding questions, enabling/disabling questions, practicing with random questions, taking tests, and viewing statistics.

## How It Works
The program is implemented in Python and follows an object-oriented approach. It utilizes the concepts of classes and objects to represent questions, question managers, practice mode, test mode, and statistics mode.

## The main components of the Interactive Learning Tool are as follows:
* Question: The Question class represents a single question. It can be a free-form question or a quiz question with multiple options. Each question has a unique ID, a question text, an answer or answer options, and statistics such as shown count and correct count.

* QuestionManager: The QuestionManager class manages the collection of questions. It allows adding new questions, toggling the status of questions (enabled or disabled), deleting all questions, and loading/saving questions from/to a file. It also provides methods for retrieving random questions based on weights and managing question IDs. The QuestionManager class also handles the interactive menu system for the user to navigate through different modes.

* PracticeMode: The PracticeMode class represents the practice mode of the Interactive Learning Tool. It allows users to practice with random questions from the enabled questions. The user can enter answers for free-form questions or select options for quiz questions. The program provides feedback on the correctness of the answers and updates the statistics for each question accordingly.

* TestMode: The TestMode class represents the test mode of the Interactive Learning Tool. Users can take a test by specifying the number of questions they want to answer. The program randomly selects questions from the enabled questions and presents them to the user. The user provides answers, and the program provides feedback on correctness. At the end of the test, the user receives a score and the results are recorded.

* StatisticsMode: The StatisticsMode class allows users to view statistics for all questions. It displays information such as question ID, active status, question text, shown count, correct count, and correct percentage. The statistics are loaded from a file and can be updated during practice or test modes.
