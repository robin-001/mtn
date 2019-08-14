from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^collect$', views.index, name='collect'),
    url(r'^disburse$', views.index, name='disburse'),
    url(r'^status$', views.index, name='status'),
]