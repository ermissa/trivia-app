import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])


    def test_delete_question(self):
        with self.app.app_context():
            question = Question.query.first()

            res = self.client().delete(f'/questions/{question.id}')
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['deleted'], question.id)


    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'] , False)
        self.assertEqual(data['message'], 'Resource not found')


    def test_create_question(self):
        new_question = {
            'question': 'Test question?',
            'answer': 'Test answer.',
            'category': 1,
            'difficulty': 3
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['created'])


    def test_400_if_question_creation_fails(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'],False)
        self.assertEqual(data['message'], 'Question, answer, category, and difficulty are required')


    def test_search_questions(self):
        search_term = 'science'

        res = self.client().post('/questions/search', json={'searchTerm': search_term})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)


    def test_400_if_search_term_not_provided(self):
        res = self.client().post('/questions/search', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


    def test_get_questions_by_category(self):
        category_id = 1

        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('current_category', data)


    def test_404_if_category_id_does_not_exist(self):
        category_id = 1000

        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])



    def test_play_quiz(self):
        quiz_params = {
            'previous_questions': [1, 2, 3],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }

        res = self.client().post('/quizzes', json=quiz_params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('question',data)


    def test_400_if_play_quiz_fails(self):
        quiz_params = {
            'previous_questions': [1, 2, 3]
        }

        res = self.client().post('/quizzes', json=quiz_params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()