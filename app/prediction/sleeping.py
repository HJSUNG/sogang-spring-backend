from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image, ImageOps

# Load the model
model = load_model('models/sleeping/keras_model.h5', compile=False)

# Load the labels
class_names = open('models/sleeping/labels.txt', "r").readlines()


def predict_sleeping(image_pil):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image_pil = image_pil.convert('RGB')

    size = (224, 224)
    image = ImageOps.fit(image_pil, size, Image.Resampling.LANCZOS)

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    return {"predictions": prediction, "predicted_label": class_name[3:]}

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