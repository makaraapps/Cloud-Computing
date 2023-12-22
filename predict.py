import numpy as np
import requests
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from io import BytesIO


# Load the model at the start of the program
MODEL_PATH = './env/makara.h5'
model = load_model(MODEL_PATH)

def preprocess_image_from_url(image_url):
    """
    Download an image from a URL, validate it, preprocess it, and convert to an array.

    Args:
    image_url (str): The URL of the image.

    Returns:
    np.array: Preprocessed image array.
    """
    response = requests.get(image_url)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")

    # Check if the content-type is of an image
    if 'image' not in response.headers.get('Content-Type', ''):
        raise Exception("URL does not point to a valid image.")

    try:
        with Image.open(BytesIO(response.content)) as img:
            img = img.resize((224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            return img_array
    except IOError:
        raise Exception("The URL does not point to a valid image file.")


def make_prediction(img_array):
    """
    Make a prediction based on the preprocessed image array.

    Args:
    img_array (np.array): The preprocessed image array.

    Returns:
    str: Predicted class label.
    """
    classes = model.predict(img_array, batch_size=8)
    class_labels = ["Bika Ambon", "Kerak Telor", "Molen", "Nasi Goreng", "Papeda Maluku", "Sate Padang", "Seblak"]
    class_index = np.argmax(classes)
    return class_labels[class_index]


