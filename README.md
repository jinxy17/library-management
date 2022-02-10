

# 迎新云参观系统 - 服务器端

## 小组
Xinya Geeks

## 仓库维护人
| 姓名 | 学号 |
| ------ | ------ |
| 金旭扬 | 2017013645 |
| 王雷捷 | 2017013648 |

## API接口（2020-09-28更新）
### 静态文件
| url | 返回 |
| ------ | ------ |
| /static/tips.html | **软件使用提示** |
| /static/info.json | **图书馆、楼层、房间层次关系及位置坐标**  |
| /static/yifu1/fplan.jpg | 逸夫馆一层平面图 |
| /static/yifu2/fplan.jpg | 逸夫馆二层平面图 |
| /static/yifu2/intloan.txt | **站点1：逸夫馆二层馆际互借处** |
| /static/yifu2/fgnst.txt | **站点2：逸夫馆二层外文科技图书借阅区** |
| /static/yifu2/chnst.txt | **站点3：逸夫馆二层中文科技图书借阅区** |
| /static/yifu3/fplan.jpg | 逸夫馆三层平面图 |
| /static/yifu3/mlib.txt | **站点4：逸夫馆三层音乐图书馆** |
| /static/yifu3/fgnpdc.txt | **站点5：逸夫馆三层外文过刊阅览区** |
| /static/yifu3/pdcnp.txt | **站点6：逸夫馆三层现刊及报纸阅览室/区** |
| /static/yifu4/fplan.jpg | 逸夫馆四层平面图 |
| /static/yifu4/chnpdc.txt | **站点7：逸夫馆四层中文过刊阅览区** |
| /static/yifu4/croom.txt | **站点8：逸夫馆四层培训教室** |
| /static/beig/fplan.jpg | 北馆G层平面图 |
| /static/beig/yjxuan.txt | **站点20：北馆G层邺架轩书店** |
| /static/beig/anc.txt | **站点11：北馆G层古籍阅览室** |
| /static/bei1/fplan.jpg | 北馆一层平面图 |
| /static/bei1/copier.txt | **站点12：北馆一层自助文印机** |
| /static/bei1/ret.txt | **站点13：北馆一层自助还书** |
| /static/bei1/circdesk.txt | **站点14：北馆一层总服务台** |
| /static/bei1/thumem.txt | **站点15：北馆一层清华印记互动体验空间** |
| /static/bei1/dscreg.txt | **站点16：北馆一层首次使用研读间/研讨间刷卡端** |
| /static/bei1/irterm.txt | **站点17：北馆一层检索终端** |
| /static/bei1/feat.txt | **站点18：北馆一层专题图书区** |
| /static/bei1/chkout.txt | **站点19：北馆一层自助借书机** |
| /static/bei2/fplan.jpg | 北馆二层平面图 |
| /static/bei2/grpdsc.txt | **站点10：北馆二层团体研讨间** |
| /static/bei3/fplan.jpg | 北馆三层平面图 |
| /static/bei3/idvdsc.txt | **站点9：北馆三层单人研读间** |
| /static/bei4/fplan.jpg | 北馆四层平面图 |
| /static/bei5/fplan.jpg | 北馆五层平面图 |

### /static/tips.html格式
```json
[
    {
        "library": String,
        "floors": [
            {
                "floor": String,
                "rooms": [ 
                    {
                        "room": String,
                        "x": int,
                        "y": int
                    },
                    ...
                ]
            },
            ...
        ]
    },
    ...
]
```

### 用户

- **用户注册**

  - url: Users/user/signup/

  - 方法：post

  - 格式：json	

    ```json
    {
    	“account”: String,
      "password": String,
      "username": String,
      "email": String,
      "major": String
    }
    ```

  - 返回：json

    - 当注册成功时，返回

      ```json
      {
        "Info": "Sign Up for %s Successfully" % username,
        "Code": 300
      }
      ```

    - 当学号已存在时，返回

      ```json
      {
        "Info": "This Student ID Has Been Registered Before",
        "Code": 200
      }
      ```

    - 当账号或密码为空时，返回

      ```json
      {
        "Info": "Empty Account or Password Are Forbidden!",
        "Code": 200
      }
      ```

      

- **用户登录**

  - url:  Users/user/signup/

  - 方法：post

  - 格式：json	

    ```json
    {
    	“account”: String,
      "password": String
    }
    ```

  - 返回：json

    - 当登录成功时，返回

      ```json
      {
        "Info": "Sign in Successfully",
        "Code": 300
      }
      ```

    - 当用户名不存在或密码错误时，返回

      ```json
      {  
        'Info': "A Request From An Illegal User",  
        'Code': 200
      }
      ```

- **修改密码**

  - url:  Users/user/change_password/

  - 方法：post

  - 格式：json	

    ```json
    {
    	“account”: String,
      "password": String,
      "new password": String
    }
    ```

  - 返回：json

    - 当修改成功时，返回

      ```json
      {
        "Info": "Change Password Successfully",
        "Code": 300
      }
      ```

    - 当用户名不存在或密码错误时，返回

      ```json
      {  
        'Info': "A Request From An Illegal User",  
        'Code': 200
      }
      ```

### 文章

- **搜索文章**

  - url: Users/article/search/

  - 方法：post

  - 格式：json	

    ```json
    {
        "uid": Long,
      	"num": Int
    }
    ```

  - 返回：json

    当查找成功时：

    当uid为-1时，返回最新的num篇文章；否则返回小于等于uid的num篇最新文章。当满足条件的文章不足num篇时，返回全部。

    返回数据中total为总共返回的文章数量。

    ```json
    {
      "Info": {
        "total": int
        "data": [{
    							"uid": article.id,
    							"title": article.title,
    							"html": article.html,
    							"pub_date": timestamp,
    							"authors": [{"name": author.account}, {}, ...]}, {}, ...],
      "Code": 300
    }
    ```


### 留言


* **发送留言**


  * url：Users/comment/add/

  * 方法：post

  * 格式：json

    ```json
      {
          "account": String,
          "password": String,
          "comment" : {
            	"articleUid":Long,
              "content": String
          }
      }
    ```

  - 返回：json

    - 当添加留言成功时，返回

      ```json
       {
          'Info': "Add the Comment Successfully",
          'Code': 300
        }
      ```

    - 当发送Json数据格式有误时，返回

      ```json
       {
          'Info': "A Request of Wrong Json Format",
          'Code': 100
        }
      ```

    - 当用户名不存在或密码错误时，返回

      ```json
       {
          'Info': "A Request From An Illegal User",
          'Code': 200
        }
      ```

    - 当文章不存在时，返回

      ```json
       {
          'Info': "A Request From An Illegal Article",
          'Code': 200
        }
      ```

* **删除留言**


  * url：Users/comment/delete/

  * 方法：post

  * 格式：json

    ```json
      {
        "uid": Long
      }
    ```

  * 返回：json


    * 当删除留言成功时，返回
    
      ```json
       {
        	'Info': "Delete the Comment ... Successfully",
        	'Code': 300
        }
      ```
    
    * 当留言不存在时，返回
    
      ```json
        {
        	'Info': "This Comment Index Does Not Exist",
        	'Code': 200
        }
      ```

  * 备注

    * 服务器端并未确认当前用户是否有权限删除本条留言。

* **查找留言**

  * url：Users/comment/delete/

  * 方法：post

  * 格式：json

    ```json
      {
          "articleUid": long,
          "uid": long, 
          "num": int
      }
    ```

  * 返回：json

      * 当查找成功时：当uid为-1时，返回最新的num条评论；否则返回小于等于uid的num条最新评论。当满足条件的评论不足num条时，返回全部。返回数据中total为总共返回的评论数量。

        ```json
          {
            "Info": {
              "total": int
              "data": [{
          							"articleUid": comment.article.id,
          							"uid": comment.id,
          							"user": comment.user.id,
          							"content": comment.content,
          							"pub_date": timestamp}, ...]
            },
            "Code": 300
          }
        ```

* **举报留言**

  * url：Users/comment/delete/

  * 方法：post

  * 格式：json

    ```json
     {
        "uid": Long
     }
    ```

  * 返回：json

    * 当举报成功时，返回

      ```json
      {
        "Info": "Report this Comment Successfully",
        "Code": 300
      }
      ```

    * 当留言不存在时，返回

      ```json
      {
      	'Info': "This Comment Index Does Not Exist",
      	'Code': 200
      }
      ```


### 应用留言

* **发送应用留言**

    * url：Users/comment/add/

    * 方法：post

    * 格式：json	

  ```json
  {
      "account": String,
      "password": String,
    	"rating": Int,
      "comment" : String
  }
  ```

    * 返回：json

      * 当添加留言成功时，返回

      ```json
      {
        'Info': "Add the Application Comment Successfully",
        'Code': 300
      }
      ```

      * 当发送Json数据格式有误时，返回

      ```json
      {
        'Info': "A Request of Wrong Json Format",
        'Code': 100
      }
      ```

      * 当用户名不存在或密码错误时，返回

      ```json
      {
        'Info': "A Request From An Illegal User",
        'Code': 200
      }
      ```

      * 当评分不为处于0-10区间的整数时，返回

      ```json
      {
        'Info': "The Rating Should Be An Interger between 0 and 10!",
        'Code': 200
      }
      ```

* **查看我的留言**

    * url：Users/appcomment/search/mycomment/

    * 方法：post

  * 格式：json	

    ```
     {
         "account": String,
         "password": String
     }
    ```

  * 返回：json

    - 当查看我的留言成功时，返回

    ```
    {
      "Info": {
    		"total": int,
    		"comment": [
    			{
    				"time”: timestamp, //用户留言发表的时间
    				"rating":int,
    				"comment": String,
    				# 当管理员留言存在时，否则直接为{}
    				"response":{
    					"time": timestamp, //管理员回复的时间
    					"responser": String, //回复的管理员的用户名
    					"comment": String //回复内容
    				} ……]
    	},
      "Code": 300
    }
    ```
    
    * 当发送Json数据格式有误时，返回
    
      ```json
      {
        'Info': "A Request of Wrong Json Format",
        'Code': 100
      }
      ```
    
    * 当用户名不存在或密码错误时，返回
    
        ```json
        {
          'Info': "A Request From An Illegal User",
          'Code': 200
        }
        ```
    
        


# Modified from: monolithic-example

The backend was bootstrapped with [`django-admin startproject app`](https://docs.djangoproject.com/en/2.2/ref/django-admin/).

## Usage

    docker build -t something .
    docker run --rm something

## Develop

### Structure

* __app__ Core settings for Django.
* __pytest.ini__ Configuration for [pytest](https://docs.pytest.org/en/latest/).
* __requirements.txt__ Package manager with `pip`.
* __requirements_dev.txt__ Package manager with `pip`, including extra tools for development.

### Tools

* `python manage.py runserver` Run this project in development mode.
* `python manage.py makemigrations` Detect changes in data schema.
* `python manage.py migrate` Apply migrations to current database.
* `pytest` Test.
* `pylint --load-plugins=pylint_django app meeting` Advanced [PEP8](https://www.python.org/dev/peps/pep-0008/) checking.

## License

MIT License
