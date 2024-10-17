from django.shortcuts import render
from django.conf import settings
from OCR.views import *
from image_preprocessor.views import *
import os
# Create your views here.



def feature_extractor(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_image.name)

        with open(image_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)


        preprocessed_image = preprocess_image(image_path)
        text = extract_text_from_image(preprocessed_image)



        context = {
            'text': text,
            'image_uploaded': True,
            'uploaded_image_name': uploaded_image.name
        }

        return render(request, 'feature_extractor.html', context)

    return render(request, 'feature_extractor.html')