#### <center>Django框架漫谈系列之一：Python web 框架的本质</center>

##### 目录

- [前言](#前言)
- [WSGI、uwsgi、uWSGI](#WSGI、uwsgi、uWSGI)
- 一个简单web服务端
- web框架的雏形



##### 前言

​	本文是Django框架漫谈系列的首篇，主要讲述python web框架的一些基础性知识，适合有一定python基础且对web后端开发感兴趣的人员。

​	通过本文， 你可以加深对web框架的一些了解：只是它们本质是什么、干了什么。



##### WSGI、uwsgi、uWSGI

​	首先我们需要了解这三个概念：WSGI、uwsgi、uWSGI。

​	**WSGI**

​	WSGI：全称为“web server gateway interface”， 也就是web服务网关接口。它是一个标准， 也可以理解为一个协议。它定义了web服务器如何与应用程序进行交互。使用它我们就可以把web应用程序和服务端对接起来。

有一点我们要知道， 在WSGI中， 有两个角色：server和application（framework）。我们常说的python的web框架有Django、flask、tornado等等， 其实指的都是application。

它的处理流程是这样的：

首先server监听端口， 收到用户请求以后进行初步处理以后调用application来完成具体的任务，最后由application返回结果给server，server在返回给用户。



