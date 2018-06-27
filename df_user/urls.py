from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'register/$', views.register),
    url(r'register_handle/$', views.register_handle),
    url(r'register_exist/$', views.register_exist),
    url(r'login/$', views.Login),
    url(r'login_handle/$', views.Login_handle),
    url(r'info/$', views.Info),
    url(r'order/$', views.order),
    url(r'site/$', views.Site),
    url(r'logout/$', views.Logout),
]