from django.shortcuts import render

# Create your views here.

def feature_extractor(request):
    return render(request, 'feature_extractor.html')