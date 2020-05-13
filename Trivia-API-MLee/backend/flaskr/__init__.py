import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  '''
  #@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''


  '''
  #@TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization')
      response. headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
      return response

  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
      categories = Category.query.all()
      formatted_categories = {category.id: category.type for category in categories}

      return jsonify({
      'success': True,
      'categories': formatted_categories,
      'total_categories': len(formatted_categories)
      })

  '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/questions', methods=['GET'])
  def get_allQuestions():
      #Pull all categories and put into formatted list
      categories = Category.query.all()
      formatted_categories=[category.format() for category in categories]

      #Prep for pogination of question results
      page = request.args.get('page', 1, type=int)
      start = (page-1)*QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      questions = Question.query.order_by(Question.id).all()

      if questions ==[]:
          abort(404)
      else:
          formatted_questions = [question.format() for question in questions]
          return jsonify({
          'success': True,
          'questions': formatted_questions[start:end],
          'total_questions': len(formatted_questions),
          'current_category': None,
          'categories': formatted_categories
              })

  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
      error = False
      try:
          #Pull question
          question = Question.query.filter(Question.id==question_id).one_or_none()
          question.delete()
      except:
          error = True
          db.session.rollback()
      finally:
          if error:
              abort(400)
          else:
              return jsonify({
              'success': True,
              'deleted': question_id
                  })

  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''
  @app.route('/questions/create', methods=['POST'])
  def create_questions():
      error = False
      # try:
      question = request.json['question']
      answer = request.json['answer']
      difficulty = request.json['difficulty']
      category = request.json['category']

     # #Check that all required data is input--if not throw bad request message
      if question == None or answer == None or difficulty==None or category == None:
          abort(400)
     #  #If so, create new record and insert into database
      else:
          new_question = Question(
          question = question,
          answer = answer,
          difficulty = difficulty,
          category = category
          )
          new_question.insert()
      # except:
      #     error = True
      #     db.session.rollback()
      #     print(sys.exc_info())
      # if error:
      #     abort(400)
      # else:
          return jsonify({
          'success': True,
          'question': question,
          'answer': answer,
          'category': category,
          'difficulty': difficulty
              })

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''
  @app.route('/questions', methods=['POST'])
  def search_questions():
      #Search for questions containing search term
      searchTerm = request.json['searchTerm']
      questions = Question.query.filter(Question.question.like('%'+searchTerm+'%')).all()

      formatted_questions = [question.format() for question in questions]
      return jsonify({
      'success': True,
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': None
          })

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_catQuestions(category_id):
      try:
          #Pull all categories and put into formatted list
          categories = Category.query.all()
          formatted_categories=[category.format() for category in categories]

          #Prep for pogination of question results
          page = request.args.get('page', 1, type=int)
          start = (page-1)*QUESTIONS_PER_PAGE
          end = start + QUESTIONS_PER_PAGE
          questions = Question.query.order_by(Question.id).filter(Question.category==category_id).all()
          formatted_questions = [question.format() for question in questions]

          if questions == []:
              abort(404)
          else:
              print(formatted_questions)
              return jsonify({
              'success': True,
              'questions': formatted_questions[start:end],
              'total_questions': len(formatted_questions),
              'current_category': category_id,
              'categories': formatted_categories
              })
      except:
          abort(422)

  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quiz():
      prev_qs = request.json['previous_questions']
      quiz_category = request.json['quiz_category']['id']
      if quiz_category==0:
          if prev_qs is not None:
              questions = Question.query.filter(Question.id.notin_(prev_qs)).all()
          else:
              questions = Question.query.all()
      else:
          if prev_qs is not None:
              questions = Question.query.filter(Question.id.notin_(prev_qs), Question.category==quiz_category).all()
          else:
              questions = Question.query.filter(Question.category==quiz_category).all()

      if questions ==[]:
          next_question=""

      else:
          next_question = random.choice(questions).format()

      return jsonify({
      'success': True,
      'question': next_question
      })

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

  @app.errorhandler(400)
  def not_found(error):
   return jsonify({
       "success": False,
       "error": 400,
       "message": "bad request"
       }), 404

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "resource not found"
          }), 404

  @app.errorhandler(422)
  def cannot_process(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "unable to process"
          }), 422

  return app

create_app().run(debug=True)
