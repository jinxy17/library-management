from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import json

INFO_JSON_PATH = "static/info.json"
STATIC_PATH = "static/"

# Create your views here.
def root(request):
    resp = '''
    <head>
    <style type="text/css">
    body {
      text-align: center;
      height: 15%;
      width: 100%;
      border-color: #afb0b2;
      border-style: solid;
      border-width: medium;
      border-collapse: collapse;
      margin-bottom: 40px;
    }
    .titles {
        color: #965454; /*#656565;*/
        text-align: center;
        font-size: 20px;
        text-decoration: none;
    }
    </style></head>
    <h1 class="titles">List of libraries:</h1>'''
    with open(INFO_JSON_PATH) as fin:
        json_obj = json.load(fin)
    for lib_obj in json_obj:
        resp += '''<a href="%s/">%s</a><br>''' % (lib_obj['library'], lib_obj['library'])
    return HttpResponse(resp)
    
def lib(request, arg1):
    resp = '''
    <head>
    <style type="text/css">
    body {
      text-align: center;
      height: 30%;
      width: 100%;
      border-color: #afb0b2;
      border-style: solid;
      border-width: medium;
      border-collapse: collapse;
      margin-bottom: 40px;
    }
    .titles {
        color: #965454; /*#656565;*/
        text-align: center;
        font-size: 20px;
        text-decoration: none;
    }
    </style></head>
    '''
    resp += '''<h1 class="titles">Library: %s</h1>''' % arg1
    with open(INFO_JSON_PATH) as fin:
        json_obj = json.load(fin)
    for lib_obj in json_obj:
        if lib_obj['library'] == arg1:
            break
    for fl_obj in lib_obj['floors']:
        resp += '''<a href="%s/">Floor %s</a><br>''' % (fl_obj['floor'], fl_obj['floor'])
    return HttpResponse(resp)

def floor(request, arg1, arg2):
    resp = '''
    <head>
    <style type="text/css">
    .block {
      text-align: center;
      border-color: #afb0b2;
      border-style: solid;
      border-width: medium;
      border-collapse: collapse;
      margin-bottom: 40px;
    }
    .titles {
        color: #965454; /*#656565;*/
        text-align: center;
        font-size: 20px;
        text-decoration: none;
    }
    </style></head>
    '''
    resp += '''<h1 class="titles">Library: %s</h1><h1 class="titles">Floor: %s</h1>''' % (arg1, arg2)
    resp += '''<div class="block">'''
    img_path = STATIC_PATH + arg1 + arg2 + '/fplan.jpg'
    resp += '''<img src="/%s" width="500"><br>''' % img_path
    resp += \
    '''
    <form method="post" action="/%s" enctype="multipart/form-data">
    更改平面图：<br>
    <input type="file" name="data" /> <br>
    <input type="submit" value="更新" />
    </form>
    ''' % img_path
    resp += '''</div>'''
    with open(INFO_JSON_PATH) as fin:
        json_obj = json.load(fin)
    for lib_obj in json_obj:
        if lib_obj['library'] == arg1:
            break
    for fl_obj in lib_obj['floors']:
        if fl_obj['floor'] == arg2:
            break
    for rm_obj in fl_obj['rooms']:
        resp += '''<div class="block">'''
        resp += '''<h2>Room %s</h2>''' % (rm_obj['room'])
        resp += '''<h3>站点图片</h3>'''
        for img in rm_obj['photos']:
            img_path = STATIC_PATH + arg1 + arg2 + '/' + img
            resp += '%s<br>' % img
            resp += '''<img src="/%s" width="200"><br>''' % img_path
            resp += \
            '''
            <form method="post" action="/Resources/submit/delpic/%s/%s/%s/%s">
            <input type="submit" value="删除">
            </form>
            ''' % (arg1, arg2, rm_obj['room'], img)
        resp += \
        '''
        <form method="post" action="/Resources/submit/addpic/%s/%s/%s" enctype="multipart/form-data">
        添加图片：<br>
        <input type="file" name="data" /> <br>
        <input type="submit" value="提交" />
        </form>
        ''' % (arg1, arg2, rm_obj['room'])

        resp += '''<h3>站点坐标</h3>'''
        resp += \
        '''
        <form method="post" action="/Resources/submit/updcod/%s/%s/%s">
        x=<input type="number" name="x" value="%d">
        y=<input type="number" name="y" value="%d">
        <input type="submit" value="更新">
        </form>
        ''' % (arg1, arg2, rm_obj['room'], rm_obj['x'], rm_obj['y'])

        resp += '''<h3>站点介绍</h3>'''
        txt_path = STATIC_PATH + arg1 + arg2 + '/%s.txt' % rm_obj['room']
        with open(txt_path) as fin:
            txt = fin.read()
        resp += \
        '''
        <form method="post" action="/%s">
        <textarea cols="50" rows="8" name="data">%s</textarea>
        <input type="submit" value="更新">
        </form>
        ''' % (txt_path, txt)
        resp += '''</div>'''

    return HttpResponse(resp)

def submit(request, arg1, arg2):
    resp = ''
    arg2 = arg2.split('/')
    with open(INFO_JSON_PATH) as fin:
        json_obj = json.load(fin)
    for lib_obj in json_obj:
        if lib_obj['library'] == arg2[0]:
            break
    for fl_obj in lib_obj['floors']:
        if fl_obj['floor'] == arg2[1]:
            break
    for rm_obj in fl_obj['rooms']:
        if rm_obj['room'] == arg2[2]:
            break
    if arg1 == 'addpic':
        path = '%s/%s%s/%s' % (getattr(settings, 'STATICFILES_DIR'), 
                                arg2[0], arg2[1], str(request.FILES['data']))
        with open(path, 'wb') as fout:
            fout.write(request.FILES['data'].read())
            resp += "Add pic success!"
        rm_obj['photos'].append(str(request.FILES['data']))
    elif arg1 == 'delpic':
        rm_obj['photos'].remove(arg2[3])
        resp += 'Remove pic success!'
    elif arg1 == 'updcod':
        rm_obj['x'] = int(request.POST['x'])
        rm_obj['y'] = int(request.POST['y'])
        resp += 'Update coodinates success!'
    with open(INFO_JSON_PATH, 'w') as fout:
        json.dump(json_obj, fout)
    return HttpResponse(resp)