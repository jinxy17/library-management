'''
Users URL Configuration
'''
from django.urls import path
from . import views
urlpatterns = [
	path('manager/signup/', views.signup_manager),
	path('manager/signin/', views.signin_manager),
	path('manager/signout/', views.signout_manager),
	path("manager/delete/<int:manager_id>/", views.delete_manager),
	path("manager/app/signin/", views.app_signin_manager),

	path("manager/managers_page/",\
		views.managers_page, name="managers_page"),

	path("manager/login_in_page/",\
		views.login_in_page, name="login_in_page"),
	path("manager/register_page/",\
		views.register_page, name="register_page"),
	path("manager/main_page/<str:page_content>/",\
		views.main_page, name="main_page"),

	path("article/all_article_page/", \
		views.all_articles_page, name="all_articles_page"),
	path("article/add_article_page/", views.add_article_page),
	path("article/add/", views.add_article),

	path("article/details/<int:article_id>/",\
		views.article_page, name="article_page"),
	path("article/comment/delete/<int:comment_id>/",\
		views.delete_comment, name="delete_comment"),
	path("article/delete/<int:article_id>/", \
		views.delete_article, name="delete_article"),

	path("appcomment/comments_page/",\
		views.comments_page, name="comments_page"),
	path("appcomment/response/<int:comment_id>/",\
		views.respond_comment, name="respond_comment")



]
