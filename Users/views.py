'''
Implemented the communication functions with the frontend
'''

import json
import datetime
import time
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Comment, Article, Author, AppComment

def gen_response(code: int, info: str):
    '''
    provide the univeral json response for communication
    with the front end'''

    return JsonResponse({
        'Info': info,
        'Code': code
    }, status=code)

def parse_request_json(request):
    '''
    provide the univeral procedure for parsing json parameters
    from the front end
    '''
    post_body = request.body.decode('utf-8') # of type string
    # print("postBody", postBody)
    try:
        post_dict = json.loads(post_body)# of type dict
        return True, post_dict
    except json.decoder.JSONDecodeError:
        return False, gen_response(100, "A Request of Wrong Json Format")
def convert_to_timestamp(now_time):
    '''
    converted the time of the format 2020-10-18T02:09:53.913Z
    to the timestamp
    '''

    now_time = str(now_time)
    dot_pos = now_time.find(".")
    trim_time = now_time[:dot_pos]
    this_date = datetime.datetime.strptime(trim_time, '%Y-%m-%d %H:%M:%S')
    timestamp = int(time.mktime(this_date.timetuple()))
    return timestamp

def legal_user(account, password, need_password=True):
    '''
    check whether the user of the account exists if need_password is False,
    otherwise, check in addition that whether the password is right or not.
    '''

    try:
        cur_user = User.objects.get(account=account)
        if need_password:
            return check_password(password, cur_user.password)
        return True
    except User.DoesNotExist:
        return False

def legal_article(article_uid):
    '''check whether the article of the id = article_uid exists'''

    try:
        Article.objects.get(id=article_uid)
        return True
    except Article.DoesNotExist:
        return False

def legal_author(account):
    '''check whether the author of the account = account exists'''

    try:
        Author.objects.get(account=account)
        return True
    except Author.DoesNotExist:
        return False

def add_article(request):
    '''add articles from the frontend, now deprecated.'''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict
    title = post_dict.get("title", "")
    content = post_dict.get("content", "")
    author_list = post_dict.get("authors", [])
    if not (title and content and author_list):
        return gen_response(200, "Empty information!")

    cur_article = Article(title=title, content=content)
    cur_article.save()

    for author in author_list:
        cur_author = None
        if not legal_author(author):
            cur_author = Author.objects.create(account=author)
        else:
            cur_author = Author.objects.get(account=author)
        cur_article.authors.add(cur_author)
    return gen_response(300, "Add the Article Successfully")

def legal_comment(uid):
    ''' check wehther the commend of id = uid exists '''

    try:
        Comment.objects.get(id=uid)
        return True
    except Comment.DoesNotExist:
        return False

def signup_user(request):
    ''' user sign up '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    account = post_dict.get("account", "")
    password = post_dict.get("password", "")
    username = post_dict.get("username", "")
    email = post_dict.get("email", "")
    major = post_dict.get("major", "")
    if not (account and password):
        return gen_response(200, "Empty Account or Password Are Forbidden!")
    encrypted_pwd = make_password(password, "Library", 'pbkdf2_sha1')
    # print("encrypted_pwd", encrypted_pwd)
    if legal_user(account, encrypted_pwd, need_password=False):
        return gen_response(200, "This Student ID Has Been Registered Before")
    User.objects.create(account=account, username=username, \
        password=encrypted_pwd, email=email, major=major)
    return gen_response(300, "Sign Up for %s Successfully" % username)

def signin_user(request):
    ''' user sign in '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    account = post_dict.get("account", "")
    password = post_dict.get("password", "")
    if not legal_user(account, password):
        return gen_response(200, "A Request From An Illegal User")
    return gen_response(300, "Sign in Successfully!")

def change_password_user(request):
    ''' changge password for user '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    account = post_dict["account"]
    password = post_dict["password"]
    new_pwd = post_dict["new password"]
    if not legal_user(account, password):
        return gen_response(200, "A Request From An Illegal User")

    cur_user = User.objects.get(account=account)
    cur_user.password = new_pwd
    cur_user.save()
    return gen_response(300, "Change Password Successfully")

def add_comment(request):
    ''' add comment for a specific article from a user '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    # check the identity of the user
    account = post_dict.get("account", "")
    password = post_dict.get("password", "")
    if not legal_user(account, password):
        return gen_response(200, "A Request From An Illegal User")
    # add comments
    cur_user = User.objects.get(account=account)
    comment = post_dict.get("comment", dict())
    article_uid = comment.get("articleUid", -1)
    if not legal_article(article_uid):
        return gen_response(200, "A Request From An Illegal Article")
    article = Article.objects.get(id=article_uid)
    Comment.objects.create(user=cur_user, content=comment.get("content", ""), article=article)
    return gen_response(300, "Add the Comment Successfully")

def report_comment(request):
    ''' report a comment of an article from the user '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    uid = post_dict.get("uid", -1)
    if not legal_comment(uid):
        return gen_response(200, "A Request For An Illegal Comment")
    cur_comment = Comment.objects.get(id=uid)
    cur_comment.report = cur_comment.report + 1
    cur_comment.save()
    return gen_response(300, "Report this Comment Successfully")

def delete_comment(request):
    ''' delete a comment of an article from a user '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    uid = post_dict.get("uid", -1)
    try:
        cur_comment = Comment.objects.get(id=uid)
        content = cur_comment.content
        cur_comment.delete()
        return gen_response(300, "Delete the Comment %s Successfully" % content)
    except Comment.DoesNotExist:
        return gen_response(200, "This Comment Index Does Not Exist")

def search_comment_by_article(request):
    ''' search comments under a given article '''

    if not Comment.objects.all():
        return gen_response(300, {"total": 0, "data": []})

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    article_uid = post_dict.get("articleUid", -1)
    if not legal_article(article_uid):
        return gen_response(200, "A Request From An Illegal Article")

    comment_uid = post_dict.get("uid", -1)
    if comment_uid == -1:
        last_comment = Comment.objects.last()
        comment_uid = last_comment.id + 1

    num = post_dict.get("num", 1)
    comments = Comment.objects.filter(id__lt=comment_uid).\
        filter(article=article_uid).order_by("-id")
    total = min(num, len(comments))
    comments = comments[:total]
    json_comments = [{
        "articleUid": comment.article.id,
        "uid": comment.id,
        "user": comment.user.username,
        "content": comment.content,
        "pub_date": convert_to_timestamp(comment.pub_date)
    } for comment in comments]
    return gen_response(300, {"total": total, "data": json_comments})

def search_article(request):
    ''' search articles before a given article id '''

    if not Article.objects.all():
        return gen_response(300, {"total": 0, "data": []})

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    article_uid = post_dict.get("uid", -1)
    if article_uid == -1:
        last_article = Article.objects.last()
        article_uid = last_article.id + 1
    num = post_dict.get("num", 1)

    articles = Article.objects.filter(id__lt=article_uid).order_by("-id")
    total = min(num, len(articles))
    articles = articles[:total]
    json_articles = [{
        "uid": article.id,
        "title": article.title,
        "url": article.url,
        "pub_date": convert_to_timestamp(article.pub_date),
        "authors": [{"name":author.account} for author in article.authors.all()]
    } for article in articles]
    return gen_response(300, {"total": total, "data": json_articles})

def search_article_by_title(request):
    ''' search articles before a given article id '''

    if not Article.objects.all():
        return gen_response(300, {"total": 0, "data": []})

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    article_uid = post_dict.get("uid", -1)
    if article_uid == -1:
        last_article = Article.objects.last()
        article_uid = last_article.id + 1
    num = post_dict.get("num", 1)

    keywords = post_dict.get("keywords", "").split()
    # print("keywords", keywords)
    articles = Article.objects.filter(id__lt=article_uid).order_by("-id")
    for keyword in keywords:
        articles = articles.filter(title__icontains=keyword).order_by("-id")

    total = min(num, len(articles))
    articles = articles[:total]
    json_articles = [{
        "uid": article.id,
        "title": article.title,
        "url": article.url,
        "pub_date": convert_to_timestamp(article.pub_date),
        "authors": [{"name":author.account} for author in article.authors.all()]
    } for article in articles]
    return gen_response(300, {"total": total, "data": json_articles})

def add_appcomment(request):
    ''' add an app comment from a user '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    # check the identity of the user
    account = post_dict.get("account", "")
    password = post_dict.get("password", "")
    if not legal_user(account, password):
        return gen_response(200, "A Request From An Illegal User")
    # add comments
    cur_user = User.objects.get(account=account)
    rating = post_dict.get("rating", 0)
    if not (isinstance(rating, int) and 0 <= rating <= 10):
        return gen_response(200, "The Rating Should Be An Interger between 0 and 10!")
    appcomment = post_dict.get("comment", "")
    AppComment.objects.create(user=cur_user, rating=rating, comment=appcomment)
    return gen_response(300, "Add the Application Comment Successfully")

def search_appcomments_by_user(request):
    ''' get all appcomments written by a specific user '''

    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict

    # check the identity of the user
    account = post_dict.get("account", "")
    password = post_dict.get("password", "")
    if not legal_user(account, password):
        return gen_response(200, "A Request From An Illegal User")
    user_id = User.objects.get(account=account).id
    appcomments = AppComment.objects.filter(user_id=user_id).order_by("timestamp")
    total = len(appcomments)
    json_comments = [{
        "timestamp": convert_to_timestamp(appcomment.timestamp),
        "rating": appcomment.rating,
        "comment": appcomment.comment,
        "response": {} if appcomment.hasResponse == 0 else {
            "time": convert_to_timestamp(appcomment.managerresponse.timestamp),
            "responser": appcomment.managerresponse.manager.account,
            "comment": appcomment.managerresponse.comment
        }
    } for appcomment in appcomments]
    return gen_response(300, {"total": total, "comments": json_comments})
