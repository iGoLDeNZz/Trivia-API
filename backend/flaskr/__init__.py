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

    question = request.form.get('question')
    answer = request.form.get('answer')
    difficulty = request.form.get('difficulty')
    category = request.form.get('category')
    search_term = request.form.get('searchTerm', None)

    if search_term is None: # We should try to add question

      if question is not None and answer is not None and difficulty is not None and category is not None:
        
        try:
          question = Question(question, answer, category, difficulty)
          db.session.add(question)
        except:
          # (error): database error occured
          return "database error occured"

        finally:
          db.session.commit()
          return jsonify(question.format())
      else:
        # (error): input error
        return

    else:
      # find the questions that has the search term in them 
      # then return them as a pagenated list

      questions = Question.query.filter(Question.question.contains(search_term)).all()
      formated_questions = [question.format() for question in questions]
      sublist = paged_list(formated_questions, 1)
      
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

    try:
      db.session.delete(question)
    
    except:
      # Handle question does not exist
      
      return "There was an error"

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

    return jsonify({
      'success': True,
      'questions': sublist,
      'total_questions': len(Question.query.all()),
      'current_category': category_id
    })


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
  def create_quiz():

    previous_questions = request.form.getlist('previous_questions')
    quiz_category = request.form.get('quiz_category', None)

    print(quiz_category)
    all_questions = []
    if quiz_category is not None:
      all_questions = Question.query.filter(Question.category==quiz_category).all()
      
    else:
      all_questions = Question.query.all()

    new_questions = [question.format() for question in all_questions if question not in previous_questions]
    
    new_question = None
    if len(new_questions) > 0: # choose only if there is a new question
      new_question = random.choice(new_questions)

    return jsonify(new_question)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    