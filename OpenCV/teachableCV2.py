import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

import IPython as ipy
# from IPython.display import Image 

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')
label_file = "./labels.txt"
labels = []
with open(label_file, "r") as f:
        labels = [line.strip().split(' ',1) for line in f]
print(model)


# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def jpgResize(image, w, h):
    #resize the image to a 224x224 with the same strategy as in TM2:
    #resizing the image to be at least 224x224 and then cropping from the center
    size = (w, h)
    return ImageOps.fit(image, size, Image.ANTIALIAS)

def jpg_path2array(jpg_path):
    image_path = jpg_path
    image = Image.open(image_path)

    image = jpgResize(image, 224, 224)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    return image_array

def run_prediction(in_image_array):

    # Normalize the image
    normalized_image_array = (in_image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    return prediction, labels[np.argmax(prediction[0])]




import cv2

import ipywidgets
from IPython.display import display as ipydisplay

import time

image_widget = ipywidgets.Image(
    format='jpg',
    width=300,
    height=400,
)
prediction_text_widget = ipywidgets.Text(description='Prediction')
ipydisplay(image_widget)
ipydisplay(prediction_text_widget)
prediction_text_widget.value = "3"
cap = cv2.VideoCapture('http://172.16.11.10:8080/stream.mjpeg')
# cap = cv2.VideoCapture('http://172.16.11.10:8080/video')

while True:
    ret, frame = cap.read()
#   cv2.imshow('Video', frame)
    # JPEG
    _, jpeg_frame = cv2.imencode('.jpg', frame)
    cam_jpeg = jpeg_frame.tobytes()
    image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
    image = jpgResize(image, 224, 224)
    
    prediction , label = run_prediction(np.asarray(image))
    
    prediction_text_widget.value = label[1]
    image_widget.value = cam_jpeg
    if cv2.waitKey(1) == 27:
        exit(0)
    ipy.display.Image(frame)
