import pymysql
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user')


@user_blueprint.route('/login', methods=['POST'])
def user_login():
    db_config = current_app.config['DB_CONFIG']
    data = request.get_json()

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT USER_ID, USER_NM, USER_TP FROM TB_COM_USER WHERE USER_ID = %s AND USER_PW = %s", (data['USER_ID'], data['USER_PW']))
        result = cursor.fetchall()

        cursor.close()

        if not result:
            return jsonify({"message": "일치하는 사용자 정보가 없습니다.", "stacd": 200}), 200
        else:
            access_token = create_access_token(identity={"USER_ID": result[0]['USER_ID'], "USER_NM": result[0]['USER_NM'], "USER_TP": result[0]['USER_TP']})
            return jsonify({"message": "로그인 성공", "stacd": 100, "accessToken": access_token, **result[0]}), 200

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()
