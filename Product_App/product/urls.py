from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='list'),
    url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<product_id>[0-9]+)/add_comment/$', views.add_comment, name='add_comment'),
    url(r'^(?P<product_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^logout_view/$', views.logout_view, name='logout_view'),
]