from flask import Blueprint

user_blueprint = Blueprint('user', __name__, url_prefix='/user')

@user_blueprint.route('/')
def user_test():
    return "Hello World!"


