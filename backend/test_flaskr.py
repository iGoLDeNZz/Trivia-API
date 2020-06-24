import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from config import database_info

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(database_info['port'], database_info["database_name_test"])
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


    # ----------------------------------
    # App Test
    # ----------------------------------

    # Testing an endpoint that is not written
    def test_non_exsting_endpoint(self):
        response = self.client().get('/Yousef')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------
    # Questions Test
    # ----------------------------------
        
    # --------------------------
    # Endpoint: '/questions' GET
    # --------------------------

    def test_get_all_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

    def test_method_not_allowed_on_questions(self):
        response = self.client().patch('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'method not allowed')
    
    def test_error_404_page_not_found_get_all_questions(self):
        res = self.client().get('/questions?page=1111')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Page not found")
        self.assertFalse(data['success'])


    # ---------------------------
    # Endpoint: '/questions' POST
    # ---------------------------

    def test_valid_search_term(self):
        param = {
            'searchTerm' : 'the'
        } 

        response = self.client().post('/questions', data = param)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

    def test_error_404_unvalid_search_term(self):
        param = {
            'searchTerm' : 'Yousef Almassad'
        } 

        response = self.client().post('/questions', data = param)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Sorry, no question contains what you have searched for.')

    def test_200_post_new_question(self):
        param = {
            'question' : 'Yousef',
            'answer' : 'Almassad',
            'difficulty' : 9000,
            'category' : 1
        } 

        response = self.client().post('/questions', data = param)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['question'], param['question'])
        self.assertEqual(data['answer'], param['answer'])
        self.assertEqual(data['difficulty'], param['difficulty'])
        self.assertEqual(data['category'], param['category'])

    def test_error_400_post_new_question(self):
        param = {
            'question' : 'Yousef Almassad',
            'difficulty' : 9000,
            'category' : 1
        } 

        response = self.client().post('/questions', data = param)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'The answer cannot be empty.')


    # -----------------------------
    # Endpoint: '/questions' DELETE
    # -----------------------------

    def test_valid_deletion(self):
        response = self.client().delete('/questions/2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['id'], 2)


        # Make sure that when you try to delete the question again it will not be
        # in the database anymore, thus,  we conclude the success of the first deletion.
        response = self.client().delete('/questions/2')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')


    def test_unvalid_deletion(self):
        response = self.client().delete('/questions/1111')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')



    # ----------------------------------
    # Category Test
    # ----------------------------------
        
    # ----------------------------------------------------
    # Endpoint: '/categories/<category_id>/questions' GET
    # ----------------------------------------------------

    def test_200_get_all_questions_for_category(self):
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)

    def test_error_404_get_all_questions_for_category(self):
        response = self.client().get('/categories/1111/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')



    # ----------------------------------
    # Category Test
    # ----------------------------------

    # -------------------------
    # Endpoint: '/quizzes' POST
    # -------------------------

    def test_valid_search_term(self):
        param = {
            'quiz_category' : 1
        } 

        response = self.client().post('/quizzes', data = param)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['category'], param['quiz_category'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()