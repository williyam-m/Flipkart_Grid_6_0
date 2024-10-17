from django.shortcuts import render
from django.conf import settings
from .models import *
from OCR.views import *
from image_preprocessor.views import *
import os
import re
from datetime import datetime, timedelta


class ProductInfoExtractor:
    def __init__(self, text):
        self.text = text
        self.today = datetime.today().date()

    def extract_EAN(self):
        match = re.search(r'\b\d{13}\b', self.text)
        return match.group(0) if match else None

    def extract_MRP(self):
        match = re.search(r'(?i)\bMRP[:\s]*Rs[.\s]*(\d+\.?\d*)\b|\bRs[.\s]*(\d+\.?\d*)\b', self.text, re.IGNORECASE)
        if match:
            return match.group(1) or match.group(2)
        return None

    def extract_dates(self):
        date_patterns = [
            r'\d{2}/\d{2}/\d{4}',  # 07/03/2029
            r'\d{2}-\d{2}-\d{4}',  # 07-03-2029
            r'\d{2} \w{3} \d{4}',  # 07 MAR 2029
            r'\w{3} \d{2} \d{4}'  # MAR 07 2029
        ]

        dates = []
        for pattern in date_patterns:
            for match in re.findall(pattern, self.text, re.IGNORECASE):
                for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d %b %Y", "%b %d %Y"):
                    try:
                        parsed_date = datetime.strptime(match, fmt).date()
                        dates.append(parsed_date)
                        break
                    except ValueError:
                        continue
        return dates

    def calculate_expiry_from_manufactured(self, manufactured_date):
        match = re.search(r'Best before[:\s]*(\d+)\s(months?|years?)', self.text, re.IGNORECASE)
        if match:
            quantity = int(match.group(1))
            unit = match.group(2).lower()
            if 'year' in unit:
                return manufactured_date + timedelta(days=quantity * 365)
            elif 'month' in unit:
                return manufactured_date + timedelta(days=quantity * 30)
        return None

    def is_valid(self, expiry_date):
        return expiry_date > self.today if expiry_date else None

    def extract_all_info(self):
        EAN = self.extract_EAN()
        MRP = self.extract_MRP()
        dates = self.extract_dates()

        manufactured_date = None
        expiry_date = None

        if len(dates) == 2:
            dates.sort()
            manufactured_date = dates[0]
            expiry_date = dates[1]
        elif len(dates) == 1:
            expiry_date = dates[0]

        if not expiry_date and manufactured_date:
            expiry_date = self.calculate_expiry_from_manufactured(manufactured_date)

        validity = self.is_valid(expiry_date)

        return {
            'EAN': EAN,
            'MRP': MRP,
            'manufactured_date': manufactured_date,
            'expiry_date': expiry_date,
            'is_valid': validity
        }






def feature_extractor(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', uploaded_image.name)

        with open(image_path, 'wb+') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)


        preprocessed_image = preprocess_image(image_path)
        text = extract_text_from_image(preprocessed_image)

        #text = "USE BY 07 MAR 2029 4067991709876 10:49 MRP: Rs. 299.00 Manufactured: 07/03/2023 Best before 18 months"
        extractor = ProductInfoExtractor(text)
        info = extractor.extract_all_info()

        feature_extract = FeatureExtract.objects.create(
            image='uploads/' + uploaded_image.name,
            EAN = info.get("EAN"),
            MRP = info.get("MRP"),
            manufactured_date = info.get("manufactured_date"),
            expiry_date = info.get("expiry_date"),
            is_valid = info.get("is_valid")
        )


        context = {
            'text': text,
            'EAN': info.get("EAN"),
            'MRP': info.get("MRP"),
            'manufactured_date': info.get("manufactured_date"),
            'expiry_date': info.get("expiry_date"),
            'is_valid': info.get("is_valid"),
            'image_uploaded': True,
            'uploaded_image_name': uploaded_image.name,
            'uploaded_image_url': feature_extract.image.url
        }

        return render(request, 'feature_extractor.html', context)

    return render(request, 'feature_extractor.html')



def history(request):
    feature_extracts = FeatureExtract.objects.all().order_by('-uploaded_at')
    return render(request, 'feature_extractor_history.html', {'feature_extracts': feature_extracts})
