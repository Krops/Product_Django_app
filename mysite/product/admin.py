from django.contrib import admin
from .models import Product,Post
# Register your models here.
from .models import Product
class PostAdmin(admin.ModelAdmin):
    search_fields = ["title"]

admin.site.register(Post, PostAdmin)