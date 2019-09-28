#### RestfulFrameWork学习笔记

基础只是：

##### restful简介

restful是一种接口编写的规范， 并不是一种协议，非强制性。它代表的是一种软件架构风格。

以此种规范写出来的接口更具识别性。

##### restful设计原则

- 总是使用https协议

- 域名

  - 可使用子域名形式：https://api.example.com  会存在csrf问题， 尽量部署在专用域名。
  - 使用URL方式： https://example.com/api/

- 版本

  - 卸载URL中：https://example.com/api/v1/
  - 请求头中 同样面临csrf引发多次请求问题。

- 路径规范

  restful是面向资源编程， 所以使用名词表示：

  https://example.com/api/v1/users/

- method:

  - GET
  - POST
  - DELETE
  - PUT
  - OPTION
  - TRACE
  - PATCH

- 过滤

  https://example.com/api/v1/users?class=3

- state code

  OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
  CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
  Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
  NO CONTENT - [DELETE]：用户删除数据成功。
  INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
  Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
  Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
  NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
  Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
  Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
  Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
  INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。

- Hypermedia API，RESTful API最好做到Hypermedia，即返回结果中提供链接，连向其他API方法，使得用户不查文档，也知道下一步应该做什么。



#### restframework框架实现

请求传递到view后， 先进入dispatch方法：

```python

```

