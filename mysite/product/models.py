from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.BooleanField('Slug')
    description = models.TextField()
    price = models.FloatField(default=0.0)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField('date created')
    modified_at = models.DateTimeField('date modified')
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,default=1)
    product = models.ForeignKey(Product,default=1)

    def __str__(self):
        return self.title

