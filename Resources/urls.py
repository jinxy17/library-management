'''
Users URL Configuration
'''
from django.urls import path
from django.urls import re_path
from . import views
urlpatterns = [
	path('',views.root),
	re_path(r'^submit/([^/]+)/(.+)$', views.submit),
	re_path(r'^([^/]+)/$', views.lib),
	re_path(r'^([^/]+)/([^/]+)/$', views.floor),
	
]
