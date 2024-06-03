from tensorflow.keras.models import load_model
import numpy as np

# 모델 및 레이블 파일 로드
model = load_model('models/blink_and_yawn/keras_model.h5')
with open('models/blink_and_yawn/labels.txt', 'r', encoding='utf-8') as f:
    labels = f.read().splitlines()

def predict_blink_and_yawn(image_pil):
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

    return {"predictions": predictions, "predicted_label": predicted_label}


# 0 눈비비기
# 1 하품
# 2 평상시
