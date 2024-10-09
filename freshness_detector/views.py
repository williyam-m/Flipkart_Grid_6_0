from django.shortcuts import render

# Create your views here.
def freshness_detector(request):
    return render(request, 'freshness_detector.html')