from . import models

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.contenttypes.models import ContentType

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CommentForm(forms.Form):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    message = forms.CharField(widget=forms.Textarea(), label = u'Комментарий')
    content_id = forms.IntegerField(widget=forms.HiddenInput())
    content_type = forms.IntegerField(widget=forms.HiddenInput())
    user = forms.IntegerField(widget=forms.HiddenInput())

        
