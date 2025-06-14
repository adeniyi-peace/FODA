from django.db import models
from sorl.thumbnail import ImageField

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=100)
    image = ImageField(upload_to='vendors/', blank=True, null=True)
    
    def __str__(self):
        return self.name