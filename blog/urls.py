from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

accounts = [
    url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^change_password/$', views.ChangePasswordView.as_view(), name='change_password'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='blog/registration/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='blog/registration/logged_out.html'), name='logout'),
]

article = [
   url(r'^list/$', views.ArticleList.as_view(), name='article-list'),
   url(r'^add/$', views.ArticleCreate.as_view(), name='article-add'),
   url(r'^(?P<pk>\d+)/$', views.ArticleUpdate.as_view(), name='article-update'),
   url(r'^(?P<pk>\d+)/delete/$', views.ArticleDelete.as_view(), name='article-delete'),
   url(r'^(?P<pk>\d+)/get/$', views.ArticleGet.as_view(), name='article-get'),
]

urlpatterns = [
    url(r'^accounts/', include(accounts)),
    url(r'^article/', include(article)),
    url(r'^home/$', views.HomePageView.as_view(), name='home'),
    url(r'^$', views.HomePageView.as_view()),
]
