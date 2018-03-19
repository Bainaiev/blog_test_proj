from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
  
class Article(models.Model):
    headline = models.CharField(max_length=100, unique=True)
    content = models.TextField() 
    tags = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return self.headline

    class Meta:
    	ordering = ('headline',)

    def get_absolute_url(self):
        return reverse('article-list')