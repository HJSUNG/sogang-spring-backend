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

@user_blueprint.route('/checkIdValidation', methods=['POST'])
def check_id_validation():
    db_config = current_app.config['DB_CONFIG']
    data = request.get_json()

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT COUNT(*) as count FROM TB_COM_USER WHERE USER_ID = %s", (data,))

        result = cursor.fetchall()

        cursor.close()

        if(result[0]['count']>0):
            return jsonify({"message": "ID 중복", "stacd": 200, }), 200
        else :
            return jsonify({"message": "사용가능", "stacd": 100, }), 200

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()

@user_blueprint.route('/signUp', methods=['POST'])
def sign_up():
    db_config = current_app.config['DB_CONFIG']
    data = request.get_json()

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("INSERT INTO TB_COM_USER VALUES(%s,%s,%s,%s,%s,%s,%s,'USER')", (data['USER_ID'],data['USER_PW'],data['USER_NM'],data['USER_BIRTH_DT'],data['USER_GENDER'],data['USER_EMAIL_ADDR'],data['USER_ADDR']))

        connection.commit()

        cursor.close()

        return jsonify({"message": "회원가입 성공", "stacd": 100, }), 200

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()