import os
from dotenv import load_dotenv
import pymysql
from flask import Blueprint, jsonify

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


load_dotenv()

db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
    'charset':'utf8mb4',
}

@user_blueprint.route('/')
def user_test():
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM TB_COM_USER")
        result = cursor.fetchall()

        cursor.close()

        return jsonify(result)

    except Exception as e:
        return jsonify({'error':e})

    finally:
        connection.close()


