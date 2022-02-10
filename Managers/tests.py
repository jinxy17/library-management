''' unit test for Managers/views.py '''
import json
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from Users.models import User, Author, Article, Comment, AppComment
from .models import Manager, ManagerResponse

class TestManagerEndPoint(TestCase):
    ''' TestCase for /Managers '''

    def __decode_json(self, response):
        self.assertEqual(1, 1)
        return json.loads(response.content.decode('utf-8'))

    def __prepare_article(self, account_index=1):
        self.assertEqual(1, 1)
        article = Article.objects.create(title="A title")
        author = Author.objects.create(account="LeijieWangTest %d" % account_index)
        article.authors.add(author)
        return article

    def __prepare_user(self):
        self.assertEqual(1, 1)
        password = "leijiewangtest"
        encrypted_pwd = make_password(password, "Library", 'pbkdf2_sha1')
        account = "2000013648"
        username = "LeijieWangTest"
        email = "wanglj17@mails.tsinghua.edu.cn"
        major = "computer science"
        user = User.objects.create(account=account, \
            password=encrypted_pwd, username=username, email=email, major=major)
        return account, password, user

    def __prepare_manager(self):
        self.assertEqual(1, 1)
        password = "leijiewangtest"
        encrypted_pwd = make_password(password, "Library", 'pbkdf2_sha1')
        account = "LeijieWangTest"
        manager = Manager.objects.create(account=account, password=encrypted_pwd)
        return account, password, manager

    def __prepare_comment(self, article=None, number=1):
        # preparation
        if not article:
            article = self.__prepare_article()
        _, _, user = self.__prepare_user()
        for i in range(number):
            Comment.objects.create(user=user,content="Hello World % i!" % i, article=article)
        self.assertEqual(Comment.objects.all().count(), number)

    def __prepare_appcomment(self, account, number=1):
        cur_user = User.objects.get(account=account)
        rating = 5
        for index in range(number):
            AppComment.objects.create(user=cur_user,\
                rating=rating, comment="It is a good application the %d-th" % index)
        self.assertEqual(AppComment.objects.all().count(), number)

    def __loginin(self):
        account, password, _ = self.__prepare_manager()
        manager_info = {
            "login_account": account,
            "login_password": password
        }
        self.client.post("/Managers/manager/signin/", data=manager_info, follow=True)
        return manager_info

    def test_signup(self):
        ''' unit test for sign up '''

        account = "LeijieWangTest"
        password = "leijiewangtest"
        manager_info = {
            "register_account": account,
            "register_password": password,
            "confirmPassword": password
        }
        # test the successful case
        self.client.post("/Managers/manager/signup/", data=manager_info)
        self.assertEqual(Manager.objects.filter(\
            account=manager_info["register_account"]).count(), 1)

        # test the registered-before case
        self.client.post("/Managers/manager/signup/", data=manager_info)
        self.assertEqual(Manager.objects.filter(account=\
            manager_info["register_account"]).count(), 1)
        Manager.objects.filter(account=manager_info["register_account"]).delete()

        # test the empty-account case
        empty_account = ""
        manager_info["register_account"] = empty_account
        self.client.post("/Managers/manager/signup/", data=manager_info)
        self.assertEqual(Manager.objects.filter(account=\
            manager_info["register_account"]).count(), 0)
        manager_info["register_account"] = account # restore

        # test the empty-password case
        empty_password = ""
        manager_info["register_password"] = empty_password
        self.client.post("/Managers/manager/signup/", data=manager_info)
        self.assertEqual(Manager.objects.filter(account=\
            manager_info["register_account"]).count(), 0)
        manager_info["register_account"] = account # restore

    def test_signin(self):
        ''' unit test for sign in '''

        account, password, _ = self.__prepare_manager()
        manager_info = {
            "login_account": account,
            "login_password": password
        }
        # test the successful case
        response = self.client.post("/Managers/manager/signin/", \
            data=manager_info, follow=True)
        # is_login = response.client.cookies["is_login"].value
        # self.assertEqual(is_login, "1:1ke7Gx:dzNJyD4qBSLguqPuZhfVgl0648xe26kSnQa6BsRyqNk")
        self.assertEqual(response.client.cookies["account"].value, account)

        # test Wrong-password case
        # wrong_password = "Wrong-password"
        # manager_info["password"] = wrong_password
        # response = self.client.post("/Managers/manager/signin/", data=manager_info)


    def test_app_signin_manager(self):
        ''' unit test for app_signin_manager'''
        account, password, _ = self.__prepare_manager()
        manager_info = {
            "account": account,
            "password": password
        }
        # test the successful case
        response = self.client.post("/Managers/manager/app/signin/",\
            data=manager_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)

        # test Wrong-password case
        wrong_password = "Wrong-password"
        manager_info["password"] = wrong_password
        response = self.client.post("/Managers/manager/app/signin/",\
            data=manager_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_signout(self):
        ''' unit test for sign out'''

        # prepare
        manager_info = self.__loginin()
        # test the successful case
        response = self.client.post("/Managers/manager/signout/", data=manager_info, follow=True)
        self.assertEqual(response.client.cookies["account"].value, "")
        self.assertEqual(response.client.cookies["is_login"].value, "")

    def test_add_article(self):
        ''' unit test for add_article '''

        # prepare
        self.__loginin()
        article_info = {
            "title": "A New Article",
            "authors": "Acorn Bcorn Ccorn",
            "articleURL": "https://www.baidu.com",
        }

        # test the empty title case
        article_info["title"] = ""
        self.client.post("/Managers/article/add/", data=article_info)
        self.assertEqual(Article.objects.filter(title=article_info["title"]).count(), 0)
        self.assertEqual(Author.objects.all().count(), 0)
        article_info["title"] = "A New Article"

        # test the empty file case
        article_info["articleURL"] = ""
        self.client.post("/Managers/article/add/", data=article_info)
        self.assertEqual(Article.objects.filter(title=article_info["title"]).count(), 0)
        self.assertEqual(Author.objects.all().count(), 0)
        article_info["articleURL"] = "https://www.baidu.com"

        # test the successful case
        self.client.post("/Managers/article/add/", data=article_info)
        self.assertEqual(Article.objects.filter(title=article_info["title"]).count(), 1)
        self.assertEqual(Author.objects.all().count(), 3)

    def test_delete_article(self):
        ''' unit test for delete_article'''

        # prepare
        article_id = self.__prepare_article().id
        self.__loginin()

        # test the successful case
        self.client.post("/Managers/article/delete/%d/" % article_id)
        self.assertEqual(Article.objects.filter(id=article_id).count(), 0)

    def test_delete_comment(self):
        ''' unit test for delete_comment'''

        # prepare
        number = 5
        self.__prepare_comment(number=number)
        self.__loginin()
        # test the successful case
        self.client.post("/Managers/article/comment/delete/%d/" % number)
        self.assertEqual(Comment.objects.filter(id__lte=number).count(), number - 1)

    def test_respond_comment(self):
        ''' unit test for respond_comment'''

        # prepare
        account, _, _ = self.__prepare_user()
        appcomment_id = 5
        self.__prepare_appcomment(account=account, number=appcomment_id)
        # test successful case
        self.__loginin()
        appcomment_response = {
            "response": "Good Comment!",
        }
        self.client.post("/Managers/appcomment/response/%d/" % appcomment_id, \
            data=appcomment_response)
        # print(response.status_code)
        self.assertEqual(ManagerResponse.objects.filter(response_id=appcomment_id).count(), 1)
        self.assertEqual(AppComment.objects.get(id=appcomment_id).hasResponse, 1)
