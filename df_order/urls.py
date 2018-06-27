#coding=utf-8

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Order),
    url(r'^order_handle/$', views.Order_handle),
    url(r'pay/$', views.Pay),
]