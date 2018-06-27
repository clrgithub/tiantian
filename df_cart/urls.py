from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Cart),
    url(r'^add(\d+)_(\d+)/$', views.Add),
    url(r'^edit(\d+)_(\d+)/$', views.Edit),
    url(r'^delete(\d+)/$', views.Delete),
]
