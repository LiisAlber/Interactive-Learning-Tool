import unittest
from question import Question, QuestionManager
from stats import StatisticsMode

class TestQuizApp(unittest.TestCase):

    def test_question_creation(self):
        question = Question(True)
        question.question_text = "What's 2+2?"
        question.answer = "4"
        self.assertEqual(question.question_text, "What's 2+2?")
        self.assertEqual(question.answer, "4")

    def test_question_manager(self):        #tests questions loading
        manager = QuestionManager()
        manager.load_questions()
        self.assertTrue(len(manager.questions) >= 0)

    def test_statistics_mode(self):
        manager = QuestionManager()
        statistics = StatisticsMode(manager)
        statistics.load_statistics()
        for question in manager.questions:
            self.assertTrue(question.shown_count >= 0)      #non negative value
            self.assertTrue(question.correct_count >= 0)


if __name__ == '__main__':
    unittest.main()

