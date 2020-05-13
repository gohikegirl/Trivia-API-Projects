import os
import unittest
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
import random

from __init__ import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('postgres','localhost:5432', self.database_name)
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
    #Get Category tests-----------------------------------------------
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_404_sent_nonexistantCat(self):
        res = self.client().get('/categories/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')
    #End Category tests-------------------------------------------------

    #Get Questions (and Categories) tests-------------------------------
    def test_get_allQuestions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['categories'], True)

    def test_get_questionsByCat(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['total_questions'], 4)
        self.assertEqual(data['current_category'], 2)
        self.assertTrue(data['categories'], True)

    def test_422_sent_nonexistantCatQs(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'unable to process')

    def test_404_sent_nonexistantQs(self):
        res = self.client().get('/categories/2/questions/6')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'resource not found')
    #End Questions (and Categories) tests-----------------------------

    #Delete Tests-----------------------------------------------------
    def test_delete_questions(self):
        res = self.client().delete('/questions', json={'id':'13'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    def test_400_sent_delete_nonExistantQs(self):
        res = self.client().delete('/questions', json={'id':'100'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')
    #End Delete tests-----------------------------

    #Create tests---------------------------------------------
    def test_create_question(self):
        res = self.client().post('/questions/create', json={'question':'Who is Jarvis', 'answer': 'My dog', 'category':'3','difficulty':'1' })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['answer'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])

    def test_400_sent_missingInfo(self):
        res = self.client().post('/questions/create', json={'question':'Who is Jarvis', 'answer': 'My dog', 'category':'3', 'difficulty':''})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'bad request')

    #End create tests---------------------------------------------

    #Search tests---------------------------------------------
    def test_search_question(self):
        res = self.client().post('/questions', json={'searchTerm':'Dutch'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)

    def test_sent_noResults(self):
        res = self.client().post('/questions', json={'search':'jabber'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
    #End search tests---------------------------------------------

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
