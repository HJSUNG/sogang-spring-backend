from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image, ImageOps

# Load the model
model = load_model('models/yawn/keras_model.h5', compile=False)

# Load the labels
class_names = open('models/yawn/labels.txt', "r").readlines()

def predict_yawn(image_pil):
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

    return {"predictions": prediction, "predicted_label": class_name[2:]}


