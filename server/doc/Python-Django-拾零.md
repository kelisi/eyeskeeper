# Python-Django-拾零

## 1.模块

### 1.1 Model 数据库模块

#### 1.1.1 Model Field

https://docs.djangoproject.com/en/2.1/ref/models/fields/

```python
from django.db import models
"""CharFiled 由字符或文本组成的数据，需要存储少量的文本可使用CharField，定义CharField属性时必须告诉Django该在数据库中预留多少空间"""
text = models.CharField(max_length=200)
""""DateTimeField：记录日期和时间的数据，传递了实参auto_now_add=True，每当用户创建新的数据时，都让Django将这个属性自动设置成当前日期和时间"""
date_added = models.DateTimeField(auto_now_add=True)
"""ForeignKey:多对一的关系型"""
question = models.ForeignKey(Question, on_delete=models.CASCADE)

```

#### 1.1.2 数据更新指令

- makemigrations指令

  生成数据关系结构文件

  ```python
  """Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为一次迁移。
  迁移是 Django 对于模型定义（也就是你的数据库结构）的变化的储存形式
  它们其实也只是一些你磁盘上的文件。如果你想的话，你可以阅读一下你模型的迁移数据，它被储存在 polls/migrations/0001_initial.py 里。别担心，你不需要每次都阅读迁移文件，但是它们被设计成人类可读的形式，这是为了便于你手动修改它们。"""
  python manage.py makemigrations polls
  ```

- sqlmigrate

  ```python
  """查看迁移命令执行哪些数据库指令
  并没有真正在你的数据库中的执行迁移 - 它只是把命令输出到屏幕上，让你看看 Django 认为需要执行哪些 SQL 语句。这在你想看看 Django 到底准备做什么，或者当你是数据库管理员，需要写脚本来批量处理数据库时会很有用。"""
  python manage.py sqlmigrate polls 0001
  ```

- migrate

  选中所有还没有执行过的迁移（Django 通过在数据库中创建一个特殊的表 `django_migrations` 来跟踪执行过哪些迁移）并应用在数据库上 - 也就是将你对模型的更改同步到数据库结构上。



  迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。我们会在后面的教程中更加深入的学习这部分内容。

  ```python
  """自动执行数据库迁移并同步管理你的数据库结构的命令
  	在数据库里创建新定义的模型的数据表：
  	"""
  python manage.py migrate
  ```

#### 1.1.3 更新数据库/改变模型

1. 编辑 `models.py` 文件，改变模型。
2. 运行 [`python manage.py makemigrations`](https://docs.djangoproject.com/zh-hans/2.1/ref/django-admin/#django-admin-makemigrations) 为模型的改变生成迁移文件。
3. 运行  [`python manage.py migrate`](https://docs.djangoproject.com/zh-hans/2.1/ref/django-admin/#django-admin-migrate) 来应用数据库迁移

注：**数据库迁移被分解成生成和应用两个命令是为了让你能够在代码控制系统上提交迁移数据并使其能在多个应用里使用；**这不仅仅会让开发更加简单，也给别的开发者和生产环境中的使用带来方便。

#### 1.1.4 field 查找功能（SQL WHERE）

https://docs.djangoproject.com/zh-hans/2.1/topics/db/queries/#field-lookups-intro

```python
Entry.objects.filter(pub_date__lte='2006-01-01')
#translates (roughly) into the following SQL:
#SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';
```

#### 1.1.5 F()

https://docs.djangoproject.com/zh-hans/2.1/ref/models/expressions/#avoiding-race-conditions-using-f

### 1.2 shell

```python
#通过以下指令进入shell终端：是因为 manage.py 会设置 DJANGO_SETTINGS_MODULE 环境变量，这个变量会让 Django 根据 mysite/settings.py 文件来设置 Python 包的导入路径）
python manage.py shell
```

​	在django的shell终端中执行

```python
from polls.models import AbstractQuestion
#若出现doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.错误,则执行以下命令
#初步判断是未导入环境变量导致没有去load installed app
import os
   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eyeskeeper.settings")

```

### 1.2 View 视图模块

#### 1.2.1 render()

载入模板，填充上下文，再返回由它生成的 [`HttpResponse`](https://docs.djangoproject.com/zh-hans/2.1/ref/request-response/#django.http.HttpResponse) 对象」是一个非常常用的操作流程。于是 Django 提供了一个快捷函数，我们用它来重写  `index()` 视图：

## 2.URL

### 2.1 url 命名空间

`polls` 应用有 `detail` 视图，可能另一个博客应用也有同名的视图。Django 如何知道 `{% url %}` 标签到底对应哪一个应用的 URL 呢？

答案是：在根 URLconf 中添加命名空间。在 `polls/urls.py` 文件中稍作修改，加上 `app_name` 设置命名空间：

```python
from django.urls import path

from . import views
#命名空间
app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```



### [`path()`](https://docs.djangoproject.com/en/2.1/ref/urls/#django.urls.path)

-  argument: [`route`](https://docs.djangoproject.com/en/2.1/intro/tutorial01/#path-argument-route)

  `route` is a string that contains a URL pattern. When processing a request, Django starts at the first pattern in `urlpatterns` and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches.

  Patterns don’t search GET and POST parameters, or the domain name. For example, in a request to `https://www.example.com/myapp/`, the URLconf will look for `myapp/`. In a request to `https://www.example.com/myapp/?page=3`, the URLconf will also look for `myapp/`.

- argument: [`view`](https://docs.djangoproject.com/en/2.1/intro/tutorial01/#path-argument-view)

  When Django finds a matching pattern, it calls the specified view function with an [`HttpRequest`](https://docs.djangoproject.com/en/2.1/ref/request-response/#django.http.HttpRequest) object as the first argument and any “captured” values from the route as keyword arguments. We’ll give an example of this in a bit.

-  argument:[`kwargs`](https://docs.djangoproject.com/en/2.1/intro/tutorial01/#path-argument-kwargs)

  Arbitrary keyword arguments can be passed in a dictionary to the target view. We aren’t going to use this feature of Django in the tutorial.

-  argument: [`name`](https://docs.djangoproject.com/en/2.1/intro/tutorial01/#path-argument-name)

  Naming your URL lets you refer to it unambiguously from elsewhere in Django, especially from within templates. This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.

## 3. 自动化测试：

### 3.1 测试代码

### 3.2 测试视图

测试工具：client

Django 提供了一个供测试使用的 [`Client`](https://docs.djangoproject.com/zh-hans/2.1/topics/testing/tools/#django.test.Client) 来模拟用户和视图层代码的交互。我们能在 `tests.py` 甚至是  [`shell`](https://docs.djangoproject.com/zh-hans/2.1/ref/django-admin/#django-admin-shell) 中使用它。

我们依照惯例从  [`shell`](https://docs.djangoproject.com/zh-hans/2.1/ref/django-admin/#django-admin-shell) 开始，首先我们要做一些在 `tests.py` 里不是必须的准备工作。第一步是在 [`shell`](https://docs.djangoproject.com/zh-hans/2.1/ref/django-admin/#django-admin-shell) 中配置测试环境:

/

 



```
$ python manage.py shell
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
```

[`setup_test_environment()`](https://docs.djangoproject.com/zh-hans/2.1/topics/testing/advanced/#django.test.utils.setup_test_environment) 提供了一个模板渲染器，允许我们为 responses 添加一些额外的属性，例如 `response.context`，未安装此 app 无法使用此功能。注意，这个方法并 *不会* 配置测试数据库，所以接下来的代码将会在当前存在的数据库上运行，输出的内容可能由于数据库内容的不同而不同。如果你的 `settings.py` 中关于 `TIME_ZONE` 的设置不对，你可能无法获取到期望的结果。如果你之前忘了设置，在继续之前检查一下。

然后我们需要导入 [`django.test.TestCase`](https://docs.djangoproject.com/zh-hans/2.1/topics/testing/tools/#django.test.TestCase) 类（在后续 `tests.py` 的实例中我们将会使用 [`django.test.TestCase`](https://docs.djangoproject.com/zh-hans/2.1/topics/testing/tools/#django.test.TestCase) 类，这个类里包含了自己的 client 实例，所以不需要这一步）:

```
>>> from django.test import Client
>>> # create an instance of the client for our use
>>> client = Client()
```

搞定了之后，我们可以要求 client 为我们工作了:

```
>>> # get a response from '/'
>>> response = client.get('/')
Not Found: /
>>> # we should expect a 404 from that address; if you instead see an
>>> # "Invalid HTTP_HOST header" error and a 400 response, you probably
>>> # omitted the setup_test_environment() call described earlier.
>>> response.status_code
404
>>> # on the other hand we should expect to find something at '/polls/'
>>> # we'll use 'reverse()' rather than a hardcoded URL
>>> from django.urls import reverse
>>> response = client.get(reverse('polls:index'))
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#39;s up?</a></li>\n    \n    </ul>\n\n'
>>> response.context['latest_question_list']
<QuerySet [<Question: What's up?>]>
```