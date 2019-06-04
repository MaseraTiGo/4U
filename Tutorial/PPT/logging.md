### python logging入门

### 目录

- [前言](#前言)
- [logging模块](#logging模块)
- [logging的基本配置](#logging的基本配置)
- [记录异常信息](#记录异常信息)
- [logging中常用类和函数](#logging中常用类和函数)
- [使用Handlers](#使用Handlers)
- [配置的其他方式](#配置的其他方式)
- [总结](#总结)



#### 前言

在我们平时码代码的过程中， bug总是绕不开的话题， 如何快速定位出来往往是我们所需要掌握的一项重要的能力。

得益于python是一门解释性语言，运行起来非常方便， 于是在开发过程中， print语句被大量的使用，在工作中遇到意料之外的问题时经常会听到：加个print啊。如此种种， 这在某些开发场景下确实效果显著且省时省力。

但是，在生产环境下， 有各种难以预料的情景，我们不可能时时刻刻盯着标准输出那个黑乎乎的框框， 更好的办法显然是记录日志。

python的标准库中为此提供了这样一个模块：logging。

logging是一个非常有用的模块， 使用它可以帮助我们更好的理解程序的流程、当有异常发生的时候， 也能通过事先设定好的标志快速的定位到问题的所在位置。

话不多说， 下面让我们开始logging之旅吧。

#### logging 模块

logging模块是python中自带的一个标准库， 这意味着你不需要额外安装。很多第三方库都使用了这个模块来记录日志。为你的程序导入logging模块很简单：

```python
import logging
```

导入之后， 不需要过多的设置你就可以开始使用它了，向下面这样。

```python
In [3]: logging.debug('logging-debug')

In [4]: logging.info('logging-info')

In [5]: logging.warning('logging-warning')
WARNING:root:logging-warning

In [6]: logging.error('logging-error')
ERROR:root:logging-error

In [7]: logging.critical('logging-critical')
CRITICAL:root:logging-critical
```

默认 logging用五种级别来表示事件的严重程度， 依次为：	DEBUG、INFO、WARNING、ERROR和CRITICAL。严重程度如名称一样， 依次递增。

你可能注意到上面logging.debug和logging.info并没有打印出信息， 这是因为logging的默认级别是warning， 也就是说只有问题严重程度在warning及以上才会被打印。

当然， 这个级别是可以设定的， 我们将在下一小节里讲到。

我们在细看一下这些输出， 不难发现， 它们都是由问题的级别加上root然后加上传入的信息组合而成。这里的root实际上是记录器logger的名称，由logging模块默认给出。同样这个也是可以修改的， 下面就进入下一小节看看logging的基本配置吧。

#### logging的基本配置

我们可以使用logging.basicConfig(**kwargs)这个方法来配置logging。

有一个需要注意的地方：如果你习惯于PEP8的编程规范， 可能会对logging模块里面的函数、方法的命名感到‘纠结’，因为它采用的是驼峰命名法。这是有“历史原因”的，这个logging是从java的日志包Log4j那里‘领养’的。想知道更多的信息可以点击[这里](<https://wiki.python.org/moin/LoggingPackage>, 'logging_package')。

对于loggging.basicConfig来说，常用的几个参数及说明如下：

- level：指定需要记录的问题严重级别。
- filename：日志输入的文件名。
- filemode：日志以哪种方式写入。默认是：a，即追加模式。
- format：日志信息的格式。

下面我们还是来看例子。

注意， 如果你是在交互式解释器中敲代码， 此时你需要重启一个解释器， 这是因为logging.basicConfig一般来说只应该被调用一次，在你使用之前logger记录器之前。

```python
logging.basicConfig(level=logging.DEBUG, filename=r'd:\cz.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.debug('this is a debug info')

logging.warning('this is a warning info')

logging.critical('this is a critical info')
```

在解释器中运行上面的代码会发现没有任何输出， 这是因为我们把信息都输入到了'd:\cz.log'里面去了，打开看一看：

```latex
2019-06-04 09:06:52,843 - root - DEBUG - this is a debug info
2019-06-04 09:07:08,158 - root - WARNING - this is a warning info
2019-06-04 09:07:26,210 - root - CRITICAL - this is a critical info
```

结合输出我们来细看一下。

在basicConfig里我们把上面说的几个常用的参数都用上了， level的值实际上是一个int型的常量， 这个在logging的源代码里面可以看到， 如下：

```python
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
```

filename、filemode比较简单， 不再赘述， 着重看一下format（这里其实我还是比较纠结的， 毕竟format也是一个python的关键字， 这里用起来，感觉怪怪的）。

format是用来格式化输出信息的， 这个已经说过， 如上面我们的日志显示的那样， 我们只需要给出想要记录的信息的名称即可，我们来看一下常用的：

%(name)s: logger记录器的名称

%(levelname)s: 问题严重级别

%(pathname)s: 调用日志记录文件的完整路径（此处为相对于调用地方的路径）

%(filename)s: 调用文件的名称

%(asctime)s: 日志记录的时间

%(message)s: 自定义传入的信息

%(threadName): 线程的名称

%(process)d: 进程的ID

我们需要记录什么格式的信息， 照样写就ok了。

还有些其它的LogRecord属性可自行查看logging源码。

#### 记录异常信息

作为日志， 当然需要有记录异常信息的能力， 譬如说Traceback信息， 这对于我们定位和解决问题非常重要， 异常发生时应当被记录下来。

logging模块为此提供了两种方式， 我们一起来看一看。

1. exc_info关键字参数

   ```python
   import logging
   test_dict = {'a': 'apple', 'b': 'ball'}
   try:
       c = test_dict['c']
   except Exception as _:
       logging.error('exception occurred', exc_info=True)
   ```

   exc_info 默认是None不记录异常信息的， 这里我们将其设置为True表示记录， 运行会有下面的输出：

   ```python
   Traceback (most recent call last):
     File "<ipython-input-9-5bab06f011c1>", line 3, in <module>
       c = test_dict['c']
   KeyError: 'c'
   ```

2. exception函数

   ```python
   import logging
   test_dict = {'a': 'apple', 'b': 'ball'}
   try:
       c = test_dict['c']
   except Exception as _:
       logging.exception('exception occurred')
   ```

   效果与之前的是一样的。

其实一点都不奇怪......因为你去看一眼源代码会发现， exception实际调用的就是上面一个error然后把exc_info设置为True......

所以， 还是要养成多看源码的习惯。



#### logging中的常用类和函数

到目前为止， 我们所使用的都是logging提供的默认记录器root，实际工作中， 我们肯定是要根据自己的需要做一些定制， 这就需要用到一些logging中的类和函数了。

常用的类有这么几个：

Logger：我们将使用这个类的对象来调用函数进行日志记录的相关操作。

LogRecord：Logger（记录器）会自动创建LogRecord对象， 这个对象包含了要记录事件的所有信息， 如之前我们用到的时间、级别、信息等。

Handler：Handler负责将日志记录发送到所需要输入的地方， 如控制台亦或是日志文件。它是StreamHandler、FileHandler等handler的父类（世界上， StreamHandler还是FileHandler的父类）。

Formatter：这个与之前basicConfig里的format参数作用一致， 就是用来定制我们想要记录信息的格式。

我们多数时候都在与logger类的对象打交道，logger类的对象一般使用logging中的函数 getLogger(name)来实例化的，这里有一点当我们使用同一个name来实例化logger对象时， 返回的是同样的logger对象， 这样也就避免了我们在不同的模块之前传递logger的对象了。

如下面这个例子：

我们新建两个测试脚本。

```python
# logging_test_001.py
import logging
from logging_test_002 import test
logger = logging.getLogger('dante')
logger.error('test_001 error occurred!')
print('test_001-------->', id(logger))
test()

```

```python 
# logging_test_002.py
import logging
def test():
    logger = logging.getLogger('dante')
    print('test_002-------->', id(logger))
    logger.error('logging_test_002 error occurred!')
```

当我们运行logging_test_001.py的时候，会有以下输出：

```shell
logging_test_001 error occurred!
test_001--------> 2727091120112
test_002--------> 2727091120112
logging_test_002 error occurred!
```

两个logger的id是一样的， 说明是同一个对象。

此外还有一点需要注意， 我们的错误输出信息仅仅只有传入的信息这一部分， 相对于之前logging.error('xxx')简单了许多， 显示一般来说， 这点信息过于简单，令人困惑了， 所以我们需要对这个logger对象进行一些配置， 让它输出我们想要的。

但是， 我们并不能像配置root（之前的logger对象）那样使用basicConfig，我们需要使用本小结介绍的Handlers和Formatters来定制我们自己的logger。

Note：有一点比较重要， 在此说一下：我们应该使用模块级别的logger， 而且传入\_\_name\_\_来实例化一个logger对象(_\_name\_\_是python一个内建的变量， 值是当前模块的名称)。这样我们查看日志的时候就可以清楚的知道是哪一个模块出现了问题。

#### 使用Handlers

通过Handlers我们可以定制日志记录格式以及信息输出到哪个地方（控制台、文件等）。更进一步我们可以为一个logger添加多个handler，为每个handler设置不同的级别， 从而将信息输出到不同的地方，譬如说下面这个例子， 我们将WARNING级别及以上的输出到文件，将ERROR级别的信息输出到控制台。先看一下， 例子下方就是讲解。

```python
# handlers_test.py

import logging

logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(r'd:\cz_1.log')

c_handler.setLevel(logging.ERROR)
f_handler.setLevel(logging.WARNING)

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.debug('this is a debug info')
logger.info('this is a info info')
logger.warning('this is a warning info')
logger.error('this is an error info')
```

首先我们实例化了一个logger对象，接着分别通过StreamHandler和FileHandler实例化出了c_handler和f_handler

,其中FileHandler需要至少传入一个参数：日志文件存储位置。

接下来又为两个handler分别设置了事件严重级别，之后针对每个handler定制不同的格式输出， 然后通过setFormatter来进行设置。

当handler设置完后， 我们需要把他们添加到logger里面， 最后就是记录日志信息了。

简单点来说整个流程就是：

创建logger---创建一个或多个handler---设置handler（输出格式、记录级别）---在logger中添加handler---记录日志。

我们在运行logger.level(level为事件的级别）时， 会自动创建LogRecord，之前讲过，还记得么。LogRecord中包含所有信息，然后传递给各个handler， 每个handler在根据对应的设置完成日志的信息的控制台输出或者文件记录，

运行上面的脚本， 在控制台会输出：

```shell
__main__ - ERROR - this is an error info
```

当前文件夹内会生成cz_1.log, 内容为：

```note
2019-06-04 14:12:55,375 - __main__ - WARNING - this is a warning info
2019-06-04 14:12:55,375 - __main__ - ERROR - this is an error info
```

至此， logging的基本用法已经讲解完了， 你现在就可以开始为你的程序、项目定制输出自己想要的日志了。



#### 配置的其他方式

除此了上面的配置方面之外， 实际上还有两种配置方法。

一种是通过创建一个配置文件， 并用logging.config.fileConfig(xxx)（xxx为配置文件路径）加载。

config.conf文件配置方式：

```config
[loggers]
keys=dante,root
[handlers]
keys=chandler, fhandler
[formatters]
keys=cformat, fformat
[logger_root]
level=DEBUG
handlers=
[logger_dante]
level=WARNING
handlers=chandler, fhandler
qualname=dante
[handler_chandler]
class=StreamHandler
level=ERROR
formatter=cformat
args=(sys.stdout,)
[handler_fhandler]
class=FileHandler
level=DEBUG
formatter=fformat
args=('cz_1.log', )
[formatter_cformat]
format=%(name)s - %(levelname)s - %(message)s
[formatter_fformat]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

这里有点需要注意， root这个logger不添加的话会报错。

用法如下：

```python
import logging
import logging.config

logging.config.fileConfig(fname=r'.\config.conf', disable_existing_loggers=True)

logger = logging.getLogger('dante')
logger.warning('this is a warning info')
logger.error('this is an error info')
```

对照着上面的例子，很容易看懂， 不再多说。

另一种是创建一个字典， 里面是具体的配置信息， 通过logging.config.dictConfig(xxx)(xxx为对应的字典)加载。

```python
config_dict = {
        'version': 1,
        'formatters': {
            'c_format' : {
                'format' : '%(name)s - %(levelname)s - %(message)s',
            },
            'f_format': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers' : {
            'c_handler' : {
                'class' : 'logging.StreamHandler',
                'formatter' : 'c_format',
                'level' : 'ERROR',
                'stream'  : 'ext://sys.stdout',
            },
            'f_handler': {
                'class': 'logging.FileHandler',
                'formatter': 'f_format',
                'level': 'WARNING',
                'filename': 'cz_1.log'
            }
        },
        'loggers' : {
            'dante' : {
                'level' : 'DEBUG',
                'handlers': ['c_handler', 'f_handler']
            },
        },
    }
```

使用方式：

```python
import logging
import logging.config

logging.config.dictConfig(config_dict)
logger = logging.getLogger('dante')
logger.warning('this is a warning info')
logger.error('this is an error info')
```

特别注意两者都需要事先导入logging.config。



#### 总结

一篇下来， 你会发现这个logging的使用还是很简单的， 作用却是一点也不小，如果你还在print来调试不妨试试这个logging。在你的项目中用起来吧，它会让你满意的。

本文相关的代码：[here][https://github.com/MaseraTiGo/4U/tree/master/codes/tutorial_codes/logging]