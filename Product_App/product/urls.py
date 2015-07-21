from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.products, name='products'),
    url(r'^(?P<slug>\w+)/$', views.detail, name='detail'),
    url(r'^(?P<slug>\w+)/vote/$', views.vote, name='vote'),
]