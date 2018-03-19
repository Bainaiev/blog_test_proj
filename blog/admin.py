from . import models

from django.contrib import admin

# Register your models here.

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('headline', 'author', 'posted')
	list_per_page = 20
	ordering = ('headline',)