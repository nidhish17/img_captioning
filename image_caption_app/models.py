from django.db import models
from django.conf import settings
# Create your models here.

class Tag(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class CaptionedImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="media/")
    caption = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption
