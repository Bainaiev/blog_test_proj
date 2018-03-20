from . import models

from django.contrib import admin

# Register your models here.

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('headline', 'author', 'posted')
    list_per_page = 20
    ordering = ('headline',)

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'text')
    list_per_page = 20
    ordering = ('user',)