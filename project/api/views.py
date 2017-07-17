# project/api/views.py

from flask import Blueprint, jsonify, request, make_response, render_template
from sqlalchemy import exc

from project.api.models import User
from project import db


# Instantiate users blueprint
users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {
        'status': 'failure',
        'message': 'User does not exist',
    }

    try:
        user = User.query.filter_by(id=int(user_id)).first()

        if not user:
            return make_response(jsonify(response_object)), 400
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at
                }
            }
            return make_response(jsonify(response_object)), 200
    except ValueError:
        return make_response(jsonify(response_object)), 400


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all user details"""
    users = User.query.all()
    users_list = []
    for user in users:
        user_object = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        users_list.append(user_object)

    response_object = {
        'status': 'success',
        'data': {'users': users_list}
    }

    return make_response(jsonify(response_object)), 200


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    """Add user to database"""
    post_data = request.get_json()

    if not post_data:
        response_object = {
            'status': 'failure',
            'message': 'Invalid POST Payload',
        }
        return make_response(jsonify(response_object)), 400

    username = post_data.get('username')
    email = post_data.get('email')

    if not username or not email:
        response_object = {
            'status': 'failure',
            'message': 'Invalid JSON Keys',
        }
        return make_response(jsonify(response_object)), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        response_object = {
            'status': 'failure',
            'message': 'Email already in use',
        }
        return make_response(jsonify(response_object)), 400

    try:
        new_user = User(username, email)
        db.session.add(new_user)
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'failure',
            'message': 'Unknown database error',
        }
        return make_response(jsonify(response_object)), 400

    response_object = {
        'status': 'success',
        'message': '%s added!' % email,
    }
    return make_response(jsonify(response_object)), 201

@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()

    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('index.html', users=users)

