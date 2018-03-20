from . import forms
from . import models

from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from django.contrib.contenttypes.models import ContentType


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = models.Article.objects.all()
        context['nav'] = 'home'
        return context

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    form_class = forms.ProfileForm
    template_name = 'blog/registration/profile.html'

    def get(self, request, *args, **kwargs):
        u = request.user
        data = { 
            'username' : u.username,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
        }
        form = self.form_class(data, instance=u)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        u = request.user
        form = self.form_class(request.POST, instance=u)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        return render(request, self.template_name, {'form': form})

class SignUpView(View):
    form_class = forms.SignUpForm
    template_name = 'blog/registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('home'))
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    form_class = PasswordChangeForm
    template_name = 'blog/registration/change_password.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect(reverse('profile'))
        else:
            messages.error(request, 'Please correct the error below.')
        return render(request, self.template_name, {'form': form})

@method_decorator(login_required, name='dispatch')
class ArticleList(ListView):
    context_object_name = 'articles'
    template_name = 'blog/article/list.html'
    
    def get_queryset(self):
        return models.Article.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['nav'] = 'articles'
        return context

@method_decorator(login_required, name='dispatch')
class ArticleCreate(CreateView):
    model = models.Article
    fields = ['headline', 'content', 'tags']
    template_name = 'blog/article/add.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class ArticleUpdate(UpdateView):
    model = models.Article
    fields = ['headline', 'content', 'tags']
    template_name = 'blog/article/update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdate, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

@method_decorator(login_required, name='dispatch')
class ArticleDelete(DeleteView):
    model = models.Article
    success_url = reverse_lazy('article-list')
    template_name = 'blog/article/delete.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDelete, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

class ArticleGet(TemplateView):
    template_name = 'blog/article/get.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = models.Article.objects.get(pk=self.kwargs['pk'])
        comments = article.comments.all()
        context['article'] = article
        context['comments'] = comments
        return context

@method_decorator(login_required, name='dispatch')
class CommentCreate(View):
    form_class = forms.CommentForm
    template_name = 'blog/comment/add.html'

    def get(self, request, *args, **kwargs):
        article = models.Article.objects.get(pk=self.kwargs['pk'])
        parent_id = self.kwargs['parent_id']
        comments = article.comments.all()
        initial = { 
            'user': request.user.id,
            'parent_id': parent_id,
            'content_id' : article.id,
            'content_type': ContentType.objects.get_for_model(article).id,
        }
        form = self.form_class(initial)
        return render(request, self.template_name, {'form': form, 'article': article, 'comments': comments})

    def post(self, request, *args, **kwargs):
        article = models.Article.objects.get(pk=self.kwargs['pk'])
        comments = article.comments.all()
        form = self.form_class(request.POST)
        if form.is_valid():
            content_id = form.cleaned_data.get('content_id')
            content_type = form.cleaned_data.get('content_type')
            parent_id = form.cleaned_data.get('parent_id')
            message = form.cleaned_data.get('message')
            user = form.cleaned_data.get('user')
            object = ContentType.objects.get(pk=content_type).get_object_for_this_type(pk=content_id)
            c = models.Comment(
                text = message,
                user = User.objects.get(pk=user),
                content_object = object
            )
            c.parent_id = parent_id
            c.save()
            return redirect(reverse('article-get', args=(self.kwargs['pk'],)), {'article': article, 'comments': comments})
        return render(request, self.template_name, {'form': form, 'article': article, 'comments': comments})
