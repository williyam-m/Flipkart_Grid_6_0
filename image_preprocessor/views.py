from django.shortcuts import render
import cv2
import numpy as np
from django.conf import settings
import os

def preprocess_image(image_path):
    # read the image
    image = cv2.imread(image_path)

    # Normalize the image (adjust brightness and contrast)
    # Convert to float32 for better precision
    image = image.astype(np.float32) / 255.0
    image = cv2.convertScaleAbs(image, alpha=1.5, beta=0)  # Adjust alpha (contrast) and beta (brightness)

    # Apply Gaussian blur to remove noise
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to binarize the image
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary_image
