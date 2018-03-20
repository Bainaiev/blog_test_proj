from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
  
class Comment(models.Model):
    path = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['path']
        db_table = 'comment'

    def __init__(self, *args, **kwargs):
        self.parent_id = None
        super(Comment, self).__init__(*args, **kwargs)

    @property
    def level(self):
        return max(0, len(self.path)/8-1)

    @property
    def html_level(self):
        return self.level * 3

    def get_absolute_url(self):
        return '%s#comment%s' % (self.content_object.get_absolute_url(), self.id)

    def __str__(self):
        return self.text

    def save(self):
        super(Comment,self).save()
        if not self.path:
            if self.parent_id:
                try:
                    parent_path = Comment.objects.get(pk=self.parent_id).path
                except ObjectDoesNotExist:
                    parent_path = ''

            else:
                parent_path = ''
            self.path = '%s%08d' % (parent_path, self.id)
            super(Comment, self).save()

class Article(models.Model):
    headline = models.CharField(max_length=100, unique=True)
    content = models.TextField() 
    tags = models.CharField(max_length=100, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateField(db_index=True, auto_now_add=True)
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ('headline',)

    def get_absolute_url(self):
        return reverse('article-list')