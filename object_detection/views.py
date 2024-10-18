from django.shortcuts import render

# Create your views here.
def object_detection(request):
    return render(request, 'object_detection.html')
