from django.contrib import admin
from .models import Product
# Register your models here.]
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('Date information', {'fields': ['created_at'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'created_at','was_published_recently')
    list_filter = ['created_at']
    search_fields = ["name"]

admin.site.register(Product, PostAdmin)