from tensorflow.keras.models import load_model
import numpy as np

# 모델 및 레이블 파일 로드
model = load_model('models/sleeping/keras_model.h5')
with open('models/sleeping/labels.txt', 'r') as f:
    labels = f.read().splitlines()

def predict_sleeping(image_pil):
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


# C1: 두다리 굽히고 배 위에 손 얹어두고 자기
# C2: 스스로 팔베고 베개 끼고 자기
# C3: 팔 올리고 자기
# C4: 다리에 무언가를 끼고 자기
# C5: 정자세
# C6: 옆으로 자기
# C7: 정자세로 배위에 손 두기
# C8: 한쪽만 굽힌 다리-앞
# C9: 스스로 팔베기-옆
# C10: 웅크림
# C11: 한쪽만 굽힌 다리-옆
# C12: 스스로 팔베기-앞
# C13: 엎어져서 자기
# C14: 역동적인 자세