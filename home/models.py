from django.db import models

# Create your models here.
class Images(models.Model):
    name = models.CharField(max_length=10,null=True,blank=True)
    image = models.ImageField(upload_to='gallery')

    def __str__(self):
        return self.name

