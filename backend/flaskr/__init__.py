import os
from flask import Flask, request, abort, jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from werkzeug.exceptions import HTTPException
from models import setup_db, Question, Category



QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response



    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            formatted_categories = {category.id: category.type for category in categories}
            return jsonify({
                'categories': formatted_categories
            })
        except Exception as e:
            print(e)
            internal_server_error()

    

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        category_id = request.args.get('category_id', 0, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        print(f'category id : {category_id} , page : {page}')

        # If category_id is greater than 0, filter questions by category
        if category_id > 0:
            questions = Question.query.filter(Question.category == category_id).all()
        else:
            questions = Question.query.all()

        if not questions:
            not_found('Resource not found')

        formatted_questions = [question.format() for question in questions]
        current_category = None
        categories = Category.query.all()
        formatted_categories = {category.id: category.type for category in categories}
        return jsonify({
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
            'current_category': current_category
        })


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if not question:
            return not_found(f'Resource not found')

        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })



    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        question_text = body.get('question')
        answer_text = body.get('answer')
        category_id = body.get('category')
        difficulty_score = body.get('difficulty')

        if not (question_text and answer_text and category_id and difficulty_score):
            return bad_request('Question, answer, category, and difficulty are required')

        question = Question(
            question=question_text,
            answer=answer_text,
            category=category_id,
            difficulty=difficulty_score
        )
        question.insert()

        return jsonify({
            'success': True,
            'created': question.id
        })



    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')

        if not search_term:
            return bad_request('Search term is required')

        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len(formatted_questions)
        })



    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        category = Category.query.get(category_id)

        if category is None:
            return not_found('Resource not found')

        questions = Question.query.filter(Question.category == category_id).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': category.type
        })



    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        if quiz_category is None:
            return bad_request('Quiz category is required')

        if quiz_category['id'] != 0:
            questions = Question.query.filter(Question.category == quiz_category['id'],~Question.id.in_(previous_questions)).all()
        else:
            questions = Question.query.filter(~Question.id.in_(previous_questions)).all()

        if not questions:
            return jsonify({
                'success': True,
                'question': None
            })

        random_question = random.choice(questions)

        return jsonify({
            'success': True,
            'question': random_question.format()
        })            



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(message):
        return jsonify({
            'success': False,
            'error': 400,
            'message': message
        }), 400
    
    @app.errorhandler(404)
    def not_found(message):
        return jsonify({
            'success': False,
            'error': 404,
            'message': message
        }), 404

    @app.errorhandler(422)
    def unprocessable(message):
        return jsonify({
            'success': False,
            'error': 422,
            'message': message
        }), 422

    @app.errorhandler(500)
    def internal_server_error():
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500


    return app

