from django.contrib import admin
from .models import Product
# Register your models here.]
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name',               {'fields': ['name']}),
        ('Slug',               {'fields': ['slug']}),
        ('Description',               {'fields': ['description']}),
        ('Price',               {'fields': ['price']}),
       # ('Date information', {'fields': ['created_at'], 'classes': ['collapse']}),
       # ('Date modified', {'fields': ['modified_at'], 'classes': ['collapse']}),
    ]
    readonly_fields = ['created_at']
    list_display = ('name', 'created_at','modified_at','was_published_recently')
    list_filter = ['created_at']
    search_fields = ["name"]

admin.site.register(Product, PostAdmin)