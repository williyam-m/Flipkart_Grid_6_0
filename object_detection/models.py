from django.db import models

# Create your models here.
class ObjectDetect(models.Model):
    image = models.ImageField(upload_to='uploads/')
    object_count = models.IntegerField(default=0)

    uploaded_at = models.DateTimeField(auto_now_add=True)