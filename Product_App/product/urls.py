from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.products, name='products'),
    url(r'^(?P<slug>[a-z]+)/$', views.detail, name='detail'),
    #url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<slug>[a-z]+)/add_comment/$', views.add_comment, name='add_comment'),
    url(r'^(?P<slug>[a-z]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<slug>[a-z]+)/show_more_comments/$', views.show_more_comments, name='show_more_comments'),
    #url(r'^(?P<slug>[a-z]+)(?:sort=([a-z]+)/)?$', views.table_view, name='sort'),
    url(r'^logout_view/$', views.logout_view, name='logout_view'),
]