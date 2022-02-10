'''
Users URL Configuration
'''
from django.urls import path
from . import views
urlpatterns = [
    path('user/signup/', views.signup_user),
    path('user/signin/', views.signin_user),
    path('user/change_password/', views.change_password_user),

    path('comment/add/', views.add_comment),
    path('comment/delete/', views.delete_comment),
    path('comment/report/', views.report_comment),
    path('comment/search/article/', views.search_comment_by_article),

    path('article/add/', views.add_article),
    path('article/search/title/', views.search_article_by_title),
    path('article/search/', views.search_article),


    path('appcomment/add/', views.add_appcomment),
    path('appcomment/search/mycomment/', views.search_appcomments_by_user)
]
