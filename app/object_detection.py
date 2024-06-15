from flask import Blueprint, jsonify, request, current_app
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import pytz
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import pymysql

from app.prediction.blink_and_yawn import predict_blink_and_yawn
from app.prediction.sleeping import predict_sleeping
from app.prediction.facial_emotion import predict_facial_emotion
from app.prediction.yawn import predict_yawn
from app.prediction.neck_and_waist import predict_neck_and_waist
from app.prediction.eye_rubbing import predict_eye_rubbing


objectDetection_blueprint = Blueprint('objectDetection', __name__, url_prefix='/api/objectDetection')

@objectDetection_blueprint.route('/startDetection', methods=['POST'])
@jwt_required()
def start_detection():
    db_config = current_app.config['DB_CONFIG']

    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    test_type = data['test_type']

    current_user = get_jwt_identity()
    print(current_user)

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("SELECT MAX(uid) as max_pk FROM TB_DETECTION_MASTER")
        result = cursor.fetchall()

        detection_no = result[0]["max_pk"] + 1

        cursor.execute("INSERT INTO TB_DETECTION_MASTER(uid, USER_ID, START_DTTM, END_DTTM, TEST_TP) VALUES (%s,%s, %s, null, %s)", (detection_no, current_user["USER_ID"], now.strftime("%Y-%m-%d %H:%M:%S"), data['test_type']))

        connection.commit()
        cursor.close()

        return jsonify({"message": "검사 시작", "stacd": 100, "detection_no": detection_no, "start_dttm" : now.strftime("%Y-%m-%d %H:%M:%S")}), 200

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()


@objectDetection_blueprint.route('/endDetection', methods=['POST'])
@jwt_required()
def end_detection():
    db_config = current_app.config['DB_CONFIG']

    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    detection_no = data['detection_no']

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("UPDATE TB_DETECTION_MASTER SET END_DTTM = %s WHERE uid = %s", (now.strftime("%Y-%m-%d %H:%M:%S"), detection_no))

        connection.commit()
        cursor.close()

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()

    return jsonify({
        'success': True,
        "message": "검사 종료",
        "end_dttm":  now.strftime("%Y-%m-%d %H:%M:%S"),
    }), 200


@objectDetection_blueprint.route('/detectNormal', methods=['POST'])
@jwt_required()
def detectNormal():
    db_config = current_app.config['DB_CONFIG']

    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    image_data_str = data['image']
    detection_no = data['detection_no']
    detection_detail_no = data['detection_detail_no']
    test_type = data['test_type']

    # base64 디코딩하여 이미지로 변환
    _, encoded = image_data_str.split(',', 1)
    image_data = base64.b64decode(encoded)

    image_pil = Image.open(BytesIO(image_data))

    prediction_yawn = predict_yawn(image_pil)
    prediction_eye_rubbing = predict_eye_rubbing(image_pil);
    prediction_facial_emotion = predict_facial_emotion(image_pil)

    print(prediction_yawn['predicted_label'])
    print(prediction_eye_rubbing['predicted_label'])
    print(prediction_facial_emotion['predicted_label'])


    # 판정 결과 정보를 DB에 저장

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("INSERT INTO TB_DETECTION_DETAIL VALUES (%s,%s,%s,%s,%s)", (detection_no, detection_detail_no, "yawn", prediction_yawn['predicted_label'], now.strftime("%Y-%m-%d %H:%M:%S")))
        cursor.execute("INSERT INTO TB_DETECTION_DETAIL VALUES (%s,%s,%s,%s,%s)", (detection_no, detection_detail_no, "eye_rubbing", prediction_eye_rubbing['predicted_label'], now.strftime("%Y-%m-%d %H:%M:%S")))
        cursor.execute("INSERT INTO TB_DETECTION_DETAIL VALUES (%s,%s,%s,%s,%s)", (detection_no, detection_detail_no, "facial_emotion", prediction_facial_emotion['predicted_label'], now.strftime("%Y-%m-%d %H:%M:%S")))

        connection.commit()
        cursor.close()

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()

    return jsonify({
        'success': True,
        'judge_result': {
            'judge_dttm': now.strftime("%Y-%m-%d %H:%M:%S"),
            "yawn": prediction_yawn['predicted_label'],
            "eye_rubbing": prediction_eye_rubbing['predicted_label'],
            "facial_emotion": prediction_facial_emotion['predicted_label'],
        },
        'message': 'Image received and processed successfully'
    }), 200

@objectDetection_blueprint.route('/detectSleeping', methods=['POST'])
@jwt_required()
def detectSleeping():
    db_config = current_app.config['DB_CONFIG']

    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    image_data_str = data['image']
    detection_no = data['detection_no']
    detection_detail_no = data['detection_detail_no']
    test_type = data['test_type']

    # base64 디코딩하여 이미지로 변환
    _, encoded = image_data_str.split(',', 1)
    image_data = base64.b64decode(encoded)

    image_pil = Image.open(BytesIO(image_data))

    prediction_sleeping = predict_sleeping(image_pil)

    print(prediction_sleeping['predicted_label'])

    # 판정 결과 정보를 DB에 저장

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("INSERT INTO TB_DETECTION_DETAIL VALUES (%s,%s,%s,%s,%s)", (detection_no, detection_detail_no, "sleeping", prediction_sleeping['predicted_label'], now.strftime("%Y-%m-%d %H:%M:%S")))

        connection.commit()
        cursor.close()

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()

    return jsonify({
        'success': True,
        'judge_result': {
            'judge_dttm': now.strftime("%Y-%m-%d %H:%M:%S"),
            "sleeping" : prediction_sleeping['predicted_label'],
        },
        'message': 'Image received and processed successfully'
    }), 200

@objectDetection_blueprint.route('/detectPose', methods=['POST'])
@jwt_required()
def detectPose():
    db_config = current_app.config['DB_CONFIG']

    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    image_data_str = data['image']
    detection_no = data['detection_no']
    detection_detail_no = data['detection_detail_no']
    test_type = data['test_type']

    # base64 디코딩하여 이미지로 변환
    _, encoded = image_data_str.split(',', 1)
    image_data = base64.b64decode(encoded)

    image_pil = Image.open(BytesIO(image_data))

    prediction_neck_and_waist = predict_neck_and_waist(image_pil)

    print(prediction_neck_and_waist['predicted_label'])

    # 판정 결과 정보를 DB에 저장

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        cursor.execute("INSERT INTO TB_DETECTION_DETAIL VALUES (%s,%s,%s,%s,%s)", (detection_no, detection_detail_no, "neck_and_waist", prediction_neck_and_waist['predicted_label'], now.strftime("%Y-%m-%d %H:%M:%S")))

        connection.commit()
        cursor.close()

    except Exception as e:
        return jsonify({'error': e})

    finally:
        connection.close()

    return jsonify({
        'success': True,
        'judge_result': {
            'judge_dttm': now.strftime("%Y-%m-%d %H:%M:%S"),
            "neck_and_waist": prediction_neck_and_waist['predicted_label'],
        },
        'message': 'Image received and processed successfully'
    }), 200