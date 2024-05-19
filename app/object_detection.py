from flask import Blueprint, jsonify, request
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import random # 테스트용 점수 생성
import pytz

objectDetection_blueprint = Blueprint('objectDetection', __name__, url_prefix='/api/objectDetection')

@objectDetection_blueprint.route('/sendImage', methods=['POST'])
def sendImage():
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    image_data_str = data['image']
    print(image_data_str)

    # base64 디코딩하여 이미지로 변환
    _, encoded = image_data_str.split(',', 1)
    image_data = base64.b64decode(encoded)

    image_pil = Image.open(BytesIO(image_data))

    image_pil.show()

    # 학습된 Yolo Model들을 통한 자세 판정

    # 판정 결과 정보를 DB에 저장

    return jsonify({
        'success': True,
        'judge_result': {
            'judge_dttm': now.strftime("%Y-%m-%d %H:%M:%S"),
            'case1': round(random.random(),3)
        },

        'message': 'Image received and processed successfully'}), 200
