import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Actor, Movie, db_drop_and_create_all, setup_db
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app

  app = Flask(__name__)

  setup_db(app)
  # db_drop_and_create_all()  
  # CORS(app)
  CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  
  @app.route('/')
  def hello_world():
    return('hello world!')


  # @app.route('/movies', methods=['GET'])
  # # @requires_auth('get:movies')
  # # def get_movies(payload):
  # def get_movies():
  #   movies = Movie.query.all()
  #   formatted_movies = [movie.format() for movie in movies]
  #   return jsonify({
  #     'success': True, 
  #     'movies':formatted_movies
  #   })

  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('get:actors')
  def get_actor(payload,actor_id):
  # def get_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
      abort(404)
      
    return jsonify({
      'success': True, 
      'actor': actor.format()
    })

    

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_actors(payload):
  # def get_actors():
    actors = Actor.query.order_by(Actor.id).all()
    if actors is None:
      abort(404)
    formatted_actors = [actor.format() for actor in actors]
    return jsonify({
      'success': True, 
      'actors':formatted_actors
    })


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def post_actor(payload):
  # def post_actor():
    data = request.get_json()

    if 'name' not in data or data['name'] == '':
      abort(422)
   
    if 'gender' not in data or data['gender'] == '':
      abort(422)

    if 'age' not in data or data['age'] =='':
      abort(422)

    new_name = data.get('name')
    new_gender = data.get('gender')
    new_age = data.get('age')
    
    new_actor = Actor(name = new_name, gender = new_gender, age = new_age)
    new_actor.insert()

    return jsonify({
      'success': True,
    }),200


  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(payload, actor_id):
  # def delete_actor(actor_id):
    actor = Actor.query.filter_by(id = actor_id).one_or_none()
    if actor is None:
      abort(404)
    
    actor.delete()
    return jsonify({
      'success': True
    }),200


  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def patch_actor(payload, actor_id):
  # def patch_actor(actor_id):
    data = request.get_json()

    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    
    if actor is None:
      abort(404)

    if 'name' not in data or 'age' not in data or 'gender' not in data:
      abort(422)
    if data['age']=='' or data['age'] == '' or data['gender'] == '':
      abort(422)

    new_name = data['name']
    new_gender = data['gender']
    new_age = data['age']

    actor.name = new_name
    actor.age = new_age
    actor.gender = new_gender


    # if new_name !='null' and new_name!='':
    #   actor.name = new_name
    # else:
    #   abort(422)

    actor.update()

    return jsonify({
      'success':True
    }),200


  # Handling Errors

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success':False,
        'error':404,
        'message':'resource not found'
      }),404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':'unprocessable'
    }),422
      
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }),400
    
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "method not allowed"
      }), 405

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      "success": False, 
      "error": 500,
      "message": "internal server error"
      }), 500

  # @app.errorhandler(401)
  # def unauthorized(error):
  #   return jsonify({
  #     "success": False, 
  #     "error": 401,
  #     "message": "unauthorized"
  #     }), 401

  # @app.errorhandler(403)
  # def forbidden(error):
  #   return jsonify({
  #     "success": False, 
  #     "error": 403,
  #     "message": "forbidden"
  #     }), 403

  @app.errorhandler(AuthError)
  def handle_error(exception):
      print(exception.status_code)
      return jsonify({
        "sucess": False,
        "error": exception.error['code'],
        "description": exception.error['description'],
        "status_code": exception.status_code
      }), exception.status_code
  # @app.errorhandler(AuthError)
  # def unauthorized(error):
  #   return jsonify({
  #     'success': False,
  #     'error': 401,
  #     'message': 'unauthorized'
  # }, 401)

  return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug = True)