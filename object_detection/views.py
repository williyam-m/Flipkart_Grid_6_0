from django.shortcuts import render
from django.conf import settings
import os
from image_preprocessor.views import *
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np


# Load the EfficientDet model from TensorFlow Hub
model_url = "https://tfhub.dev/tensorflow/efficientdet/d0/1"
detector = hub.load(model_url)




# Function to count objects in an image
def count_objects(image_path, output_path, confidence_threshold=0.5):

    original_image, input_image = load_image(image_path)
    input_tensor = tf.convert_to_tensor(input_image, dtype=tf.uint8)
    input_tensor = input_tensor[tf.newaxis, ...]  # Add batch dimension

    # Perform inference
    detections = detector(input_tensor)

    # Extract bounding boxes and confidence scores
    boxes = detections["detection_boxes"].numpy()[0]  # Bounding boxes
    scores = detections["detection_scores"].numpy()[0]  # Confidence scores

    # Filter out detections with confidence below the threshold
    filtered_indices = np.where(scores > confidence_threshold)[0]
    filtered_boxes = boxes[filtered_indices]

    # Count the number of detected objects
    object_count = len(filtered_boxes)

    # Draw the bounding boxes on the original image
    for box in filtered_boxes:
        ymin, xmin, ymax, xmax = box
        (left, right, top, bottom) = (int(xmin * original_image.shape[1]), int(xmax * original_image.shape[1]),
                                      int(ymin * original_image.shape[0]), int(ymax * original_image.shape[0]))
        cv2.rectangle(original_image, (left, top), (right, bottom), (255, 0, 0), 2)  # Draw bounding box with color blue


    # Convert the image back to BGR before saving
    original_image_bgr = cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, original_image_bgr)  # Save the image

    return object_count

# Example usage
def object_detection(request):
    image_path = os.path.join(settings.BASE_DIR, 'freshness_detector', 'static', 'images', 'fruit-veg-bg.png')
    output_path = os.path.join(settings.BASE_DIR, 'freshness_detector', 'static', 'images', 'fruit-veg-bg-detected.png')

    object_count = count_objects(image_path, output_path)
    print(f'Number of objects detected: {object_count}')
    return render(request, 'object_detection.html', {'output_image': 'static/images/fruit-veg-bg-detected.png'})
