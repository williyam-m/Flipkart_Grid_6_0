from django.shortcuts import render
from django.conf import settings
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Load the trained model
model_path = os.path.join(settings.BASE_DIR, 'freshness_detector', 'model', 'fruit_veg_freshness_model.h5')

model = tf.keras.models.load_model(model_path)

# Define the classes
all_classes = ['FreshApple', 'RottenApple', 'FreshBanana', 'RottenBanana', 'FreshMango', 'RottenMango',
               'FreshOrange', 'RottenOrange', 'FreshStrawberry', 'RottenStrawberry', 'FreshCarrot', 'RottenCarrot',
               'FreshTomato', 'RottenTomato', 'FreshCucumber', 'RottenCucumber', 'FreshPotato', 'RottenPotato',
               'FreshBellpepper', 'RottenBellpepper']

def predict_image(image_path):
    img = load_img(image_path, target_size=(150, 150))
    img_array = img_to_array(img)
    img_array = img_array / 255.0
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    predictions = model.predict(img_array)
    predicted_class = all_classes[tf.argmax(predictions[0])]
    return predicted_class

# Create your views here.
def freshness_detector(request):

    image = os.path.join(settings.BASE_DIR, 'freshness_detector', 'media', 'apple-rotton.jpg')

    predicted_class = predict_image(image)
    print(predicted_class)
    return render(request, 'freshness_detector.html', {'predicted_class':predicted_class})


