# Smart Vision
**Demo Video Link:** https://drive.google.com/file/d/1zGRH7hZHdC5wMe0rGrF7HOlIhgulY-hb/view?usp=drive_link

![Smart Vision](/static/images/smart-vision-top.png)

**Step-by-Step Guide to Setting Up and Running the Application**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/williyam-m/Flipkart_Grid_6_0.git
   ```
2. **Create a Virtual Environment**
    ```bash
   python -m venv venv
   ```
3. **Activate the Virtual Environment**

   - **On Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **On Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
4. **Install Required Packages**
    ```bash
   pip install -r requirements.txt
    ```
5. **Run the Application**
 
   ```bash
   python manage.py runserver
   ```
   
### Freshness Detector

![Smart Vision](/static/images/freshness-detector-img.png)
 - Predicts the freshness and identifies the class (type) of fruits and vegetables.
 - Utilizes a model I trained using a dataset from Kaggle with MobileNetV2 as the base model in TensorFlow.

### Feature Extractor

![Smart Vision](/static/images/feature-extractor-img.png)
 - Extracts product details such as MRP, EAN, manufacture date, and expiry date using OCR powered by Pytesseract.
 - Processes the text to validate the expiry date of the product.


### Object Detection

![Smart Vision](/static/images/object-detection-img.png)
 - Counts and highlights products within an image.
 - Employs the EfficientDet model from TensorFlow Hub.


### Dataset For `Freshness Detector`

**Download the dataset from Kaggle.**

- Link : https://www.kaggle.com/datasets/muhriddinmuxiddinov/fruits-and-vegetables-dataset


### Pre-trained Model / Architecture for `Object Detection`

- Link : https://tfhub.dev/tensorflow/efficientdet/d0/1

### Tesseract OCR Engine for Optical Character Recognition

- Tesseract : https://github.com/tesseract-ocr/tesseract

- Pytesseract : https://pypi.org/project/pytesseract/


![Smart Vision](/static/images/smart-vision-bottom.png)


## References and Resources

 - Django Documentation: https://docs.djangoproject.com/
 - Python Official Documentation: https://docs.python.org/3/
 - Keras : https://keras.io/
 - TensorFlow : https://www.tensorflow.org/
 - MobileNetV2 : https://keras.io/api/applications/mobilenet/
 - OpenCV : https://opencv.org/
 - SQLite : https://www.sqlite.org/index.html