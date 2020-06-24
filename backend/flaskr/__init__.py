import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 100


# app = Flask(__name__)

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO (DONE): Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
  
  '''
  @TODO (DONE): Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  

  # ------------------ 
  # @MARK: Helper functions
  # ------------------ 
  QUESTION_PER_PAGE = 10
  def paged_list(list, page):
    start = (page - 1) * QUESTION_PER_PAGE
    end = start + QUESTION_PER_PAGE

    return list[start:end]



  # ------------------ 
  # MARK: End points
  # ------------------ 

  '''
  @TODO (Done): 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories')
  def get_all_categories():
    categories = Category.query.order_by(Category.id).all()
    formated_categories = [category.format() for category in categories]

    return jsonify({
      'success': True,
      'categories': formated_categories
    })


  '''
  @TODO (Done): 
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
  def get_all_questions():
      
    page = request.args.get('page', 1, type=int)

    questions = Question.query.order_by(Question.id).all()
    formated_questions = [question.format() for question in questions]
    sublist = paged_list(formated_questions, page)

    # There are no questions to return
    if len(sublist) == 0:
      abort(404)

    categories = Category.query.all()
    formated_categories = [category.format() for category in categories]

    return jsonify({
      'success': True,
      'questions': sublist,
      'total_questions': len(Question.query.all()),
      'categories': formated_categories,
      'current_category': None
    })    

  '''
  @TODO (DONE): 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score. 

  @TODO (DONE):
  Also, the endpoint should get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def add_new_question():

    question = request.form.get('question', None)
    answer = request.form.get('answer', None)
    difficulty = request.form.get('difficulty', None)
    category = request.form.get('category', None)
    search_term = request.form.get('searchTerm', None)

    if search_term is None: # We should try to add question

      if question is None:
        abort(400, {'message': 'The question cannot be empty.'})

      if answer is None:
        abort(400, {'message': 'The answer cannot be empty.'})

      if difficulty is None:
        abort(400, {'message': 'The difficulty cannot be empty.'})

      if category is None:
        abort(400, {'message': 'The category cannot be empty.'})

        
        try:
          question = Question(question, answer, category, difficulty)
          db.session.add(question)
        except:
          abort(422)
        finally:
          db.session.commit()
          return jsonify(question.format())

    else:
      # find the questions that has the search term in them 
      # then return them as a pagenated list

      questions = Question.query.filter(Question.question.contains(search_term)).all()
      formated_questions = [question.format() for question in questions]
      sublist = paged_list(formated_questions, 1)
      
      if len(sublist) == 0:
        abort(404, {'message': 'Sorry, no question contains what you have searched for.'})

      return jsonify({
        'success': True,
        'questions': sublist,
        'total_questions': len(Question.query.all()),
        'current_category': None
      })
      
  

  '''
  @TODO (Done): 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    
    question = Question.query.get(question_id)
    print(f'\n\nThe question is: {question}\n\n')

    if question is None:
      abort(404)

    try:
      db.session.delete(question)
    
    except:
      abort(422)
    finally:
      db.session.commit()
    
    return jsonify(question.format())


  '''
  @TODO (Done): 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions', methods=['GET'])
  def all_questions_for_category(category_id):

    questions = Question.query.filter(Question.category==category_id).all()
    formated_questions = [question.format() for question in questions]
    sublist = paged_list(formated_questions, 1)

    if len(sublist) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': sublist,
      'total_questions': len(Question.query.all()),
      'current_category': category_id
    })


  '''
  @TODO (Done): 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def create_quiz():

    previous_questions = request.form.getlist('previous_questions', None)
    quiz_category = request.form.get('quiz_category', None)

    print(quiz_category)
    all_questions = []
    if quiz_category is not None and quiz_category != "":
      all_questions = Question.query.filter(Question.category==quiz_category).all()
    else:
      all_questions = Question.query.all()

    new_questions = [question.format() for question in all_questions if question not in previous_questions]
    
    new_question = None
    if len(new_questions) > 0: # choose only if there is a new question. No need to abort.
      new_question = random.choice(new_questions)

    return jsonify(new_question)

  # ------------------ 
  # MARK: Error handlers
  # ------------------ 


  '''
  @TODO : 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  def getCustomErrorMessage(error, fallback_message):
    try:
      return error.description["message"] # custom error message
    except TypeError:
      return fallback_message # fallback to default


  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": getCustomErrorMessage(error, "bad request")
      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": getCustomErrorMessage(error, "resource not found")
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": getCustomErrorMessage(error, "method not allowed")
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": getCustomErrorMessage(error, "unprocessable")
      }), 422
  
  return app

    