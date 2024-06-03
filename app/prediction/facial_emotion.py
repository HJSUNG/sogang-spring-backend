from tensorflow.keras.models import load_model
import numpy as np

# 모델 및 레이블 파일 로드
model = load_model('models/facial_emotion/keras_model.h5')
with open('models/facial_emotion/labels.txt', 'r') as f:
    labels = f.read().splitlines()

def predict_facial_emotion(image_pil):
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


# 0 happy
# 1 sad
