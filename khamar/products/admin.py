from django.contrib import admin
from . import models
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('Name',)}
    list_display = ['Name', 'slug']

admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Product)
admin.site.register(models.Review)
