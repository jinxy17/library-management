''' unit test for Users/views.py '''

import json
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from .models import User, Author, Article, Comment, AppComment

class TestUserEndPoint(TestCase):
    ''' TestCase for /Users '''

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

    def __prepare_comment(self, article=None, number=1):
        # preparation
        if not article:
            article = self.__prepare_article()
        _, _, user = self.__prepare_user()
        for i in range(number):
            Comment.objects.create(user=user,\
                content="Hello World % i!" % i, article=article)
        self.assertEqual(Comment.objects.all().count(), number)
    def __prepare_appcomment(self, account, number=1):
        cur_user = User.objects.get(account=account)
        rating = 5
        for index in range(number):
            AppComment.objects.create(user=cur_user,\
                rating=rating, comment="It is a good application the %d-th" % index)
        self.assertEqual(AppComment.objects.all().count(), number)

    def test_signup(self):
        ''' unit test signup function '''

        account = "LeijieWangTest"
        password = "leijiewangtest"
        user_info = {
            "account": account,
            "password": password,
            "email": "wanglj17@mails.tsinghua.edu.cn",
            "major": "computer science"
        }
        # test the successful case
        response = self.client.post("/Users/user/signup/", \
            data=user_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        self.assertEqual(User.objects.filter(account=user_info["account"]).count(), 1)

        # test the registered-before case
        response = self.client.post("/Users/user/signup/",\
            data=user_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(account=user_info["account"]).count(), 1)
        User.objects.filter(account=user_info["account"]).delete()

        # test the empty-account case
        empty_account = ""
        user_info["account"] = empty_account
        response = self.client.post("/Users/user/signup/",\
            data=user_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(account=empty_account).count(), 0)
        user_info["account"] = account # restore

        # test the empty-password case
        empty_password = ""
        user_info["password"] = empty_password
        response = self.client.post("/Users/user/signup/",\
            data=user_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(account=user_info["account"]).count(), 0)
        user_info["password"] = password

        # test the wrong-json-format case
        response = self.client.post("/Users/user/signup/",\
            data="adfad", content_type="application/json")
        # "adfad" illegal json format
        self.assertEqual(response.status_code, 100)

    def test_signin(self):
        ''' unit test for signin function '''

        account, password, _ = self.__prepare_user()
        user_info = {
            "account": account,
            "password": password
        }
        # test the successful case
        response = self.client.post("/Users/user/signin/",\
            data=user_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)

        # test Wrong-password case
        wrong_password = "Wrong-password"
        user_info["password"] = wrong_password
        response = self.client.post("/Users/user/signin/",\
            data=user_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        ''' unit test for add_comment function '''

        # preparation
        article = self.__prepare_article()
        account, password, _ = self.__prepare_user()
        comment_info = {
            "account": account,
            "password": password,
            "comment": {
                "articleUid": article.id,
                "content": "Hello World!"
            }
        }
        # test the successful case
        response = self.client.post("/Users/comment/add/",\
            data=comment_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        self.assertEqual(Comment.objects.filter(id=1).count(), 1)

        # test the wrong password case
        wrong_password = "Wrong-password"
        comment_info["password"] = wrong_password
        response = self.client.post("/Users/comment/add/",\
            data=comment_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        comment_info["password"] = password # restore

        # test the nonexist article case
        wrong_article_uid = -1
        comment_info["comment"]["articleUid"] = wrong_article_uid
        response = self.client.post("/Users/comment/add/",\
            data=comment_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        comment_info["comment"]["articleUid"] = article.id


    def test_report_comment(self):
        ''' unit test for report_comment function '''

        self.__prepare_comment()
        # test the successful case
        response = self.client.post("/Users/comment/report/",\
            data={"uid": 1}, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        self.assertEqual(Comment.objects.get(id=1).report, 1)

        # test the illegal comment case
        wrong_comment_uid = 10
        response = self.client.post("/Users/comment/report/",\
            data={"uid": wrong_comment_uid}, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_delete_comment(self):
        ''' unit test for delete_comment function '''

        self.__prepare_comment()
        # test the successful case
        response = self.client.post("/Users/comment/delete/",\
            data={"uid": 1}, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        self.assertEqual(Comment.objects.filter(id=1).count(), 0)

        # test the illegal comment case
        wrong_comment_uid = 10
        response = self.client.post("/Users/comment/delete/",\
            data={"uid": wrong_comment_uid}, content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_comment_search_by_article(self):
        ''' unit test for search_comment_by_article function '''

        number = 5
        comment_uid = number + 1
        article = self.__prepare_article()
        search_info = {
            "articleUid": article.id,
            "uid": comment_uid,
            "num": number
        }
        # test null dataset
        response = self.client.post("/Users/comment/search/article/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        result = self.__decode_json(response)["Info"]["data"]
        self.assertEqual(len(result), 0)

        self.__prepare_comment(article=article, number=number)
        # test article non exist case
        search_info["articleUid"] = 10
        response = self.client.post("/Users/comment/search/article/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)

        # test successful case
        search_info["articleUid"] = article.id
        search_info["uid"] = number + 1
        response = self.client.post("/Users/comment/search/article/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        result = self.__decode_json(response)["Info"]["data"]
        self.assertEqual(len(result), number)

        search_info["uid"] = -1
        response = self.client.post("/Users/comment/search/article/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        result = self.__decode_json(response)["Info"]["data"]
        self.assertEqual(len(result), number)

    def test_search_article(self):
        ''' unit test for search_article function '''

        number = 5
        article_uid = number
        search_info = {
            "uid": article_uid,
            "num": number
        }
        # test the null dataset
        response = self.client.post("/Users/article/search/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        result = self.__decode_json(response)["Info"]["data"]
        self.assertEqual(len(result), 0)

        for i in range(number):
            self.__prepare_article(account_index=i)

        # test the successful case
        search_info["uid"] = number + 1
        response = self.client.post("/Users/article/search/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        result = self.__decode_json(response)["Info"]["data"]
        self.assertEqual(len(result), number)

        search_info["uid"] = -1
        response = self.client.post("/Users/article/search/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        result = self.__decode_json(response)["Info"]["data"]
        self.assertEqual(len(result), number)


    def test_add_appcomment(self):
        ''' unit test for add_appcomment function '''

        # prepare
        account, password, _ = self.__prepare_user()
        rating = 5
        appcomment_info = {
            "account": account,
            "password": password,
            "rating": rating,
            "comment": "Good Application!"
        }

        # test the successful case
        response = self.client.post("/Users/appcomment/add/",\
            data=appcomment_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        self.assertEqual(AppComment.objects.filter(id=1).count(), 1)

        # test the wrong password case
        wrong_password = "Wrong-password"
        appcomment_info["password"] = wrong_password
        response = self.client.post("/Users/appcomment/add/",\
            data=appcomment_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        appcomment_info["password"] = password # restore

        # test the illegal rating case
        for illegal_rating in [-1, 11, 1.5]:
            appcomment_info["rating"] = illegal_rating
            response = self.client.post("/Users/appcomment/add/",\
                data=appcomment_info, content_type="application/json")
            self.assertEqual(response.status_code, 200)

    def test_search_app_comments_by_user(self):
        ''' unit test for search_appcomments_by_user function '''

        # prepare
        account, password, _ = self.__prepare_user()
        number = 10
        self.__prepare_appcomment(account, number)
        search_info = {
            "account": account,
            "password": password
            }
        # test the wrong password case
        wrong_password = "Wrong-password"
        search_info["password"] = wrong_password
        response = self.client.post("/Users/appcomment/search/mycomment/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        search_info["password"] = password # restore
        # test successful case
        response = self.client.post("/Users/appcomment/search/mycomment/",\
            data=search_info, content_type="application/json")
        self.assertEqual(response.status_code, 300)
        result = self.__decode_json(response)["Info"]["comments"]
        self.assertEqual(len(result), number)
