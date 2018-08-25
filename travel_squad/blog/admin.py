from django.contrib import admin
from .models import Article, Photos, Tags

# Register your models here.
admin.site.register(Article)
admin.site.register(Photos)
admin.site.register(Tags)
