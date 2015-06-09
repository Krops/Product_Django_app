from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.BooleanField(False)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    created_at = models.DateTimeField('date created')
    modified_at = models.DateTimeField('date modified')

    