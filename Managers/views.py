''' Implemented the communication functions with the web page '''
import json
from functools import wraps
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.clickjacking import xframe_options_exempt
from Users.models import Article, Author, Comment, AppComment
from .models import Manager, ManagerResponse


def gen_response(code: int, info: str):
    '''
    provide the univeral json response for communication
    with the front end
    '''
    return JsonResponse({
        'Info': info,
        'Code': code}, status=code)

def parse_request_json(request):
    '''
    provide the univeral procedure for parsing json parameters
    from the front end
    '''
    post_body = request.body.decode('utf-8') # of type string
    try:
        post_dict= json.loads(post_body) # of type dict
        return True, post_dict
    except json.decoder.JSONDecodeError:
        return False, gen_response(100, "A Request of Wrong Json Format")

def legal_manager(account, password, need_password=True):
    '''
    check whether the manager of the account exists if need_password is False,
    otherwise, check in addition that whether the password is right or not.'''
    try:
        cur_manager = Manager.objects.get(account=account)
        if need_password:
            # print("check_password", check_password(password, cur_manager.password))
            return check_password(password, cur_manager.password)
        return True
    except Manager.DoesNotExist:
        return False

def legal_author(account):
    '''check whether the author of the account = account exists'''

    try:
        Author.objects.get(account=account)
        return True
    except Author.DoesNotExist:
        return False

def legal_article(article_uid):
    '''check whether the article of the id article_uid exists'''
    try:
        Article.objects.get(id=article_uid)
        return True
    except Article.DoesNotExist:
        return False

def check_supermanager(func):
    ''' check the login status by cookies as a decorator function '''
    @wraps(func)
    def inner(request, *args, **kwargs):
        rep = request.get_signed_cookie("is_supermanager", default="0", salt="ban")
        if rep == "1":
            return func(request, *args, **kwargs)
        return redirect("login_in_page")
    return inner

def check_login(func):
    ''' check the login status by cookies as a decorator function '''

    @wraps(func)
    def inner(request, *args, **kwargs):
        rep = request.get_signed_cookie("is_login", default="0", salt="ban")
        if rep == "1":
            return func(request, *args, **kwargs)
        return redirect("login_in_page")
    return inner

def register_page(request):
    ''' render the register page '''

    return render(request, "register_page.html")

def signup_manager(request):
    ''' manager sign up '''

    account = request.POST.get("register_account") or None
    password = request.POST.get("register_password") or None
    confirmed_pwd = request.POST.get("confirmPassword") or None
    if not (account and password and confirmed_pwd):
        return render(request, "register_page.html", \
            {"warning": "Empty password or account!", "checked": False})
    if not password == confirmed_pwd:
        return render(request, "register_page.html", \
            {"warning":
                "The confirmed password is not the same as the original password!",
                "checked": False})
    encrypted_pwd = make_password(password, "Library", 'pbkdf2_sha1')
    if legal_manager(account, encrypted_pwd, need_password=False):
        return render(request, "register_page.html", \
            {"warning": "This manager account has been registered before!", \
                "checked": False})
    Manager.objects.create(account=account, password=encrypted_pwd)
    return redirect("register_page")

@check_supermanager
def delete_manager(request, manager_id):
    ''' delete manager '''
    if Manager.objects.get(id=manager_id).account == "LibrarySuperManager":
        return redirect("managers_page") # cannot delete supermanager
    Manager.objects.filter(id=manager_id).delete()
    return redirect("managers_page")


def login_in_page(request):
    ''' render the login_in page '''
    if not legal_manager("LibrarySuperManager", "pwd", need_password=False):
        Manager.objects.create(account="LibrarySuperManager", \
            password=make_password("pwd", "Library", 'pbkdf2_sha1'))
    rep = render(request, "login_in.html")
    rep.delete_cookie("is_login")
    rep.delete_cookie("account")
    rep.delete_cookie("is_supermanager")
    return rep

def signin_manager(request):
    ''' manager signin '''
    account = request.POST.get("login_account") or None
    password = request.POST.get("login_password") or None
    if (not account) or (not password) or (not legal_manager(account, password)):
        return render(request, "login_in.html", {"warning": "A Request From An Illegal Manager"})
    rep = redirect("main_page", page_content="all_articles_page")
    rep.set_signed_cookie("is_login", "1", salt="ban", max_age=60*10)
    rep.set_cookie("account", account, max_age=60*10)
    if account == "LibrarySuperManager":
        rep.set_signed_cookie("is_supermanager", "1", salt="ban", max_age=60*10)
    else:
        rep.set_signed_cookie("is_supermanager", "0", salt="ban", max_age=60*10)
    return rep

def app_signin_manager(request):
    ''' manager signin for the frontend '''
    valid_json, post_dict = parse_request_json(request)
    if not valid_json:
        return post_dict
    account = post_dict.get("account", "")
    password = post_dict.get("password", "")
    if (not account) or (not password) or (not legal_manager(account, password)):
        return gen_response(200, "A Request From An Illegal Manager")
    return gen_response(300, "Sign in Successfully!")

@check_login
def signout_manager(request):
    ''' manager signout '''

    rep = redirect("login_in_page")
    rep.delete_cookie("is_login")
    rep.delete_cookie("account")
    rep.delete_cookie("is_supermanager")
    return rep

@check_supermanager
def managers_page(request):
    ''' return manager page'''
    managers = [ {"id": manager.id,
                 "account": manager.account
                 } for manager in Manager.objects.all()]
    return render(request, "managers_page.html", {"managers": managers})

@check_login
@xframe_options_exempt
def main_page(request, page_content="all_articles_page"):
    ''' render the main page '''

    is_supermanager = request.get_signed_cookie("is_supermanager", default="0", salt="ban")
    return render(request, "main_page.html", \
        {"is_supermanager": is_supermanager, "page_content": page_content})

@check_login
def all_articles_page(request):
    ''' render the all_articles page '''
    articles = [ {"id": article.id,
                  "title": article.title,
                  "authors": " ".join([str(author) for author in article.authors.all()]),
                  "pub_date": article.pub_date.strftime('%Y-%m-%d %H:%M:%S')}
                for article in Article.objects.all()]
    # print("articles", articles)
    return render(request, "all_articles_page.html",\
        {"articles": articles})

@check_login
def add_article_page(request):
    ''' render the add_article page '''
    return render(request, "add_article.html",\
        {"add_info": "Please enter your article information!"})

@check_login
def add_article(request):
    ''' add new articles '''

    title = request.POST.get("title")
    authors = request.POST.get("authors").split()
    article_url = request.POST.get("articleURL")
    if not (title and authors and article_url):
        return render(request, "add_article.html",\
            {"add_article_info": "Empty title or authors or URL!"})
    article = Article(title=title, url=article_url)
    article.save()
    for author in authors:
        cur_author = None
        if not legal_author(author):
            cur_author = Author.objects.create(account=author)
        else:
            cur_author = Author.objects.get(account=author)
        article.authors.add(cur_author)
    return render(request, "add_article.html",\
        {"add_article_info": "Add the article successfully!"})


@check_login
def article_page(request, article_id):
    ''' render the article page for each article '''

    if legal_article(article_id):
        cur_article = Article.objects.get(id=article_id)
        return render(request, "article_page.html", \
            {"article": cur_article,
             "articleURL": cur_article.url,
              "comments": cur_article.comments.all})
    return gen_response(code=300, info="Invalid Artilce ID")

@check_login
def delete_article(request, article_id):
    ''' delete article '''

    Article.objects.filter(id=article_id).delete()
    return redirect(reverse("all_articles_page"))

@check_login
def delete_comment(request, comment_id):
    ''' delete a comment for a given article '''

    article_id = Comment.objects.get(id=comment_id).article.id
    Comment.objects.filter(id=comment_id).delete()
    return redirect("article_page", article_id=article_id)

@check_login
def comments_page(request):
    ''' render the app comment page '''

    appcomments = []
    for appcomment in AppComment.objects.all():
        appcomment_info = {"pub_date": appcomment.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                     "id": appcomment.id,
                     "userAccount": appcomment.user.account,
                     "comment": appcomment.comment,
                     "hasResponse": appcomment.hasResponse}
        if appcomment.hasResponse == 1:
            appcomment_info["resTimestamp"] = \
                appcomment.managerresponse.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            appcomment_info["managerAccount"] = \
                appcomment.managerresponse.manager.account
            appcomment_info["resComment"] = \
                appcomment.managerresponse.comment
        appcomments.append(appcomment_info)
    return render(request, "comments_page.html", {"appcomments": appcomments})

@check_login
def respond_comment(request, comment_id):
    ''' respond app comments by managers '''

    comment = request.POST.get("response")
    account = request.COOKIES["account"]
    manager = Manager.objects.get(account=account)
    appcomment = AppComment.objects.get(id=comment_id)
    ManagerResponse.objects.create(manager=manager, response=appcomment, comment=comment)
    appcomment.hasResponse = 1
    appcomment.save()
    return redirect("comments_page")
