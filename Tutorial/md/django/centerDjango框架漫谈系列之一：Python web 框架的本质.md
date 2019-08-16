#### <center>Django框架漫谈系列之一：Python web 框架的本质</center>

##### 目录

- [前言](#前言)
- [WSGI、uwsgi、uWSGI](#WSGI、uwsgi、uWSGI)
- [web框架的雏形](#web框架的雏形)



#### 前言

<hr style="height:1px;border:none;border-top:1px solid #555555;" />

本文是Django框架漫谈系列的首篇，主要讲述python web框架的一些基础性知识，适合有一定python基础且对web后端开发感兴趣的人员。

通过本文， 你可以加深对web框架的一些了解：只是它们本质是什么、干了什么。







#### WSGI、uwsgi、uWSGI

<hr style="height:1px;border:none;border-top:1px solid #555555;" />

首先我们需要了解这三个概念：**WSGI、uwsgi、uWSGI**。



##### WSGI

WSGI：全称为“web server gateway interface”， 也就是web服务网关接口。它是一个标准， 也可以理解为一个协议。它定义了web服务器如何与应用程序进行交互。使用它我们就可以把web应用程序和服务端对接起来。

有一点我们要知道， 在WSGI中， 有两个角色：server和application（framework）。我们常说的python的web框架有Django、flask、tornado等等， 其实指的都是application。

它的处理流程是这样的：

首先server监听端口， 收到用户请求以后进行初步处理以后调用application来完成具体的任务，最后由application返回结果给server，server在返回给用户。

##### uwsgi

uwsgi是一个uWSGI服务器的自有协议， 它用于定义传输信息的类型， 每一个uwsgi packet的前4byte为传输信息的类型描述，此处不再赘诉， 感兴趣的小伙伴可以自行google。



##### uWSGI

uWSGI是一个web服务器（即上面代码中的server作用）， 它实现了WSGI标准（协议）、uwsgi协议、http等协议。





#### web框架的雏形

<hr style="height:1px;border:none;border-top:1px solid #555555;" />

```python
from wsgiref.simple_server import make_server


# application
def application(environ, start_response):
    start_response('200 ok', [('Content-Type', 'text/html')])
    return [b'hello world']


# WSGI server
with make_server('', 8080, application) as httpd:
    sa = httpd.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    import webbrowser

    webbrowser.open('http://localhost:8080')
    httpd.serve_forever()
```

在上面的代码中， 我们利用python自带的wsgiref模块启动了一个简单的server服务器。然后写了一个名为application的简单应用处理函数。运行这段代码， 会自动打开浏览器并显示'hello world'。

其中：

environ：包含了所有的请求信息。

start_response是用来返回response的头部信息， 第一个参数为状态码， 第二个为具体的头信息。

application函数的返回值实际上就是response的body中的信息。

在上面的代码中我们始终返回的都是'hello world'， 在实际场景中远比这复杂的多， 这也是django、flask等出现的原因， 然我们不必过于关注细节， 专注于快速开发。

例如， 我们访问不同的地址（url）一般来说应该有不同的回复， 我们可以对上面的代码进行一点修改：

```python
# application
def application(environ, start_response):
    start_response('200 ok', [('Content-Type', 'text/html')])
    if 'location' in environ.get('PATH_INFO', ''):
        return [b'I am in china']
    if 'say' in environ.get('PATH_INFO', ''):
        return [b'hello world']
    else:
        return [b'welcome to my index page']
```

这样一来， 当我们直接访问127.0.0.1：8000的时候， 就会显示‘welcome to my index page’， 当

访问127.0.0.1：8000/location的时候就会显示‘I am in china’， 同样， 访问127.0.0.1：8000/say的时候， 就先显示‘hello world’了。

这就实现了一个极其简陋的url路由了。

我们所遇到的框架django也好， flask也罢， 等等都是在这个基础上进行扩展的， url、view、model、template等等， 都是用于处理一个请求， 返回预期的结果。

