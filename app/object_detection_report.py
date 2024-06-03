from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
import pytz
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pymysql

objectDetectionReport_blueprint = Blueprint('objectDetectionReport', __name__, url_prefix='/api/objectDetectionReport')

@objectDetectionReport_blueprint.route('/getDetectionNoList', methods=['POST'])
@jwt_required()
def get_detection_no_list():
    db_config = current_app.config['DB_CONFIG']

    current_user = get_jwt_identity()

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("""SELECT uid, USER_ID, DATE_FORMAT(START_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') as START_DTTM,DATE_FORMAT(END_DTTM, '%%Y-%%m-%%d %%H:%%i:%%s') as END_DTTM FROM TB_DETECTION_MASTER WHERE USER_ID = %s""", (current_user['USER_ID']))
        result = cursor.fetchall()

        cursor.close()

        return jsonify({
            "stacd": 100,
            "detection_no_list": result,
        }), 200
    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()