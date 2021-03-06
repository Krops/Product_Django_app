from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.urlresolvers import reverse

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    was_published_recently.admin_order_field = 'created_at'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product:detail', args=[str(self.slug)])

class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,default=1)
    product = models.ForeignKey(Product,default=1)

    def __str__(self):
        return self.title

class Vote(models.Model):
    product = models.ForeignKey(Product,default=1)
    author = models.ForeignKey(User,default=1)
    rate = models.BooleanField('Liked')