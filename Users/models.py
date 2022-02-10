''' Models for the app Users '''

from django.db import models

class User(models.Model):
    ''' Models for Student User '''

    account = models.CharField(unique=True, max_length=10) # student ID
    username = models.CharField(default="Anonymous", max_length=10)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    major = models.CharField(max_length=20)
    def __str__(self):
        return str(self.account)

class Author(models.Model):
    ''' Author of the Article '''

    account = models.CharField(unique=True, max_length=20)
    def __str__(self):
        return str(self.account)

class Article(models.Model):
    ''' Articles posted on the app '''

    title = models.CharField(max_length=20)
    pub_date = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(Author)
    url = models.TextField(default="https://www.baidu.com")
    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    ''' Comment of articles '''

    content = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="comments", on_delete=models.CASCADE)
    report = models.IntegerField(default=0)
    def __str__(self):
        return str(self.id) + ":" + str(self.content) + "\n"

class AppComment(models.Model):
    ''' Comments for app '''

    user = models.ForeignKey(User, related_name="appcomments", on_delete=models.CASCADE)
    rating = models.IntegerField() # 用户评分
    comment = models.CharField(max_length=1000) # 用户评论
    timestamp = models.DateTimeField(auto_now_add=True) # 发布时间
    hasResponse = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user) + ":" + str(self.comment) + "\n"
