from flask_jsonschema_validator import JSONSchemaValidator
from flask import Flask, jsonify, request, redirect
import swagger
import jsonschema

from src.domain.user.user_entity import UserEntity
from src.domain.user.user_repository import UserRepository
from src.domain.user.user_service import UserService, UserNotFoundException
from src.infrastructure.storage.database.mongo_db.mongo_client import MongodbClient


import config

app = Flask(__name__, static_url_path='/static')
JSONSchemaValidator(app=app, root="schemas")

app.register_blueprint(swagger.swagger_ui_blueprint, url_prefix=swagger.SWAGGER_URL)

mongodb_client = MongodbClient()
mongodb_user_collection = mongodb_client.users
user_repository = UserRepository(mongodb_user_collection)
user_service = UserService(user_repository)


@app.route('/')
def root_url():
    return redirect('/static/docs/redoc.html')


@app.route('/v1/users', methods=['POST'])
@app.validate('user', 'user_schema')
def create():
    create_user_response = user_service.create(UserEntity.from_dict(data=request.get_json()))
    return jsonify(status='success', data={'user': create_user_response.to_dict()})


@app.route('/v1/users', methods=['GET'])
def fetch_all():
    fetch_all_response = user_service.fetch_all()
    return jsonify(status='success', data={'users': fetch_all_response.to_dict()})


@app.route('/v1/users/accounts/<string:account_id>', methods=['GET'])
def fetch_all_by_account(account_id: str):
    fetch_all_response = user_service.fetch_all_by_account(account_id)
    return jsonify(status='success', data={'users': fetch_all_response.to_dict()})


@app.route('/v1/users/<string:user_id>', methods=['GET'])
def fetch(user_id: str):
    try:
        fetch_response = user_service.fetch(user_id)
        return jsonify(status='success', data={'user': fetch_response.to_dict()})
    except UserNotFoundException:
        return jsonify(status='fail', statusCode='4020', statusDescription='user not found'), 404
    except Exception as e:
        return jsonify(status='fail', statusCode='4030', statusDescription=str(e)), 500


@app.route('/v1/users/email/<string:email>', methods=['GET'])
def fetch_by_email(email: str):
    try:
        fetch_response = user_service.fetch_by_email(email)
        return jsonify(status='success', data={'user': fetch_response.to_dict()})
    except UserNotFoundException:
        return jsonify(status='fail', statusCode='4020', statusDescription='user not found'), 404
    except Exception as e:
        return jsonify(status='fail', statusCode='4030', statusDescription=str(e)), 500


@app.route('/v1/users/<string:user_id>', methods=['PATCH'])
def update(user_id: str):
    update_response = user_service.update(user_id, UserEntity.from_dict(data=request.get_json()))
    return jsonify(status='success', data={'user': update_response.to_dict()})


@app.errorhandler(jsonschema.ValidationError)
def on_validation_error(e):
    return jsonify(
        {"status": "error", "statusCode": "4000", "statusDescription": e.message}), 400

# @app.errorhandler(Exception)
# def global_error(e):
#     return jsonify(
#         {"status": "error", "statusCode": "4050", "statusDescription": 'System Error'}), 500


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE)
