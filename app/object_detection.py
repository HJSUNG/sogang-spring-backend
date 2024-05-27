from flask import Blueprint, jsonify, request
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import random # 테스트용 점수 생성
import pytz
import numpy as np

from tensorflow.keras.models import load_model


objectDetection_blueprint = Blueprint('objectDetection', __name__, url_prefix='/api/objectDetection')

# 모델 및 레이블 파일 로드
model = load_model('models/sleeping/keras_model.h5')
with open('models/sleeping/labels.txt', 'r') as f:
    labels = f.read().splitlines()

@objectDetection_blueprint.route('/sendImage', methods=['POST'])
def sendImage():
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)

    data = request.get_json()

    image_data_str = data['image']

    # base64 디코딩하여 이미지로 변환
    _, encoded = image_data_str.split(',', 1)
    image_data = base64.b64decode(encoded)

    image_pil = Image.open(BytesIO(image_data))

    # 이미지를 RGB로 변환
    image_pil = image_pil.convert('RGB')
    # 이미지를 모델이 예상하는 크기로 조정 (예시: 224x224)
    image_pil = image_pil.resize((224, 224))

    # 이미지를 numpy 배열로 변환
    img_array = np.array(image_pil)

    # 모델로 예측
    predictions = model.predict(np.array([img_array]))

    # 예측 결과 해석
    predicted_label = labels[np.argmax(predictions)]

    print(predicted_label)
    print(predictions)
    # 판정 결과 정보를 DB에 저장 (이 부분은 생략)

    return jsonify({
        'success': True,
        'judge_result': {
            'judge_dttm': now.strftime("%Y-%m-%d %H:%M:%S"),
            'predicted_label': predicted_label
        },
        'message': 'Image received and processed successfully'
    }), 200