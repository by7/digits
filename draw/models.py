from django.db import models

# Create your models here.
class Image(models.Model):
    base64code = models.CharField(max_length=2000)
	