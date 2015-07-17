from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.products, name='products'),
    url(r'^(?P<slug>\w+)/$', views.detail, name='detail'),
    url(r'^(?P<slug>\w+)/add_comment/$', views.add_comment, name='add_comment'),
    url(r'^(?P<slug>\w+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<slug>\w+)/show_more_comments/$', views.show_more_comments, name='show_more_comments'),
]