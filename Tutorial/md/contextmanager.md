### Python中的上下文管理器

#### 目录

- 前言

- 糟糕出错了



#### 前言

本文主要讲一些关于上下文管理器的知识， 通过本文你可以了解到：

- 什么是上下文管理器
- 如何实现一个上下文管理器

适宜人群：了解python的基础知识，仅此而已。



#### 糟糕出错了

python经常用来与数据打交道（啰嗦， 哪种语言又不是呢~）， 数据可能存在于数据库、文本文件、网页等等地方， 首先要获取它，然后才能谈处理。假如我们要处理一个文本文件， 它里面包含的是一些信息。我们一般来说是这么做的：

```python
def read_file_to_lines(path):
    f = open(path, 'r')
    lines = f.readlines()
    return lines
```

上面的代码片段， 我们知识简单的读取一个文件， 并返回这个文件中内容列表。

假如我们传入了一个不存在的文件（实际环境中一点也不奇怪）， 就会出现下面这中情况：

```python
In [3]: read_file_to_lines('lover.txt')
----------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
<ipython-input-3-aec0faf6aec7> in <module>()
----> 1 read_file_to_lines('lover.txt')

<ipython-input-2-03319421d830> in read_file_to_lines(path)
      1 def read_file_to_lines(path):
----> 2     f = open(path, 'r')
      3     lines = f.readlines()
      4     return lines

FileNotFoundError: [Errno 2] No such file or directory: 'lover.txt'
```

它说文件找不到。

呵呵， 这还不简单？异常处理不就是来干这些事的么？当然， 我们改动一下：

```python
import sys
def read_file_to_lines(path):
    try:
    	f = open(path, 'r')
    except Exception as e:
        print('exception occurred! reason is:', e)
        sys.exit()
    lines = f.readlines()
    return lines
```

这里并没有仅仅捕获FileNotFoundError这一个异常， 而是所有， 实际开发中尽量不要如此， 要划分细一些。

如果发生异常程序就中断退出。

这样写是没有问题的， 它也满足了我们的需求。

但是，此处应有但是， 不然这篇文章咋办......

我们完全可以用更简洁的方式来实现它，也就是我们本篇要讲的上下文管理器。



#### 什么是上下文管理器

说直白点， 就是帮我们处理好执行某些操作可能会出现的问题。例如上面说到的文件读取，还有网络连接、数据库连接等等，我们在写这些相关的程序的时候， 往往都需要打开一个连接（创建一个对象）用完之后需要关关闭这个连接， 这一切都可以在上下文管理器中完成。而不用每次都显式处理一遍。

还有个更直白的说法：就是实现了\_\_enter\_\_和\_\_exit\_\_这两个方法的类。

总而言之就是帮我处理可能出现的各种问题。

其实open就是一个内置的上下文管理器，我们可以这么使用：

```ptyhon
def read_file_to_lines(path):
    with open(path, 'r') as f
        lines = f.readlines()
        return lines
```

对， 就是使用了一个关键字with。

注意，即便你这么写， 你传入一个不存在的文件依旧会报错， 因为这个上下文管理器并没有对异常进行处理。那么我们想让它能处理异常，就像上面那样，该怎么做呢？

来吧， 实现我们自己的上下文管理器！



#### 实现自己的上下文管理器

上一小结已经说了，实现了\_\_enter\_\_和\_\_exit\_\_这两个方法的类就算一个上下文装饰器，enter方法用来执行以下进入该上下文管理器的操作， 同样， exit用来执行处理完毕后， 也就是with里的代码块执行完后， 退出时所要执行的操作。

针对开篇的那个问题， 我们要在文件不存在的时候，打印一句话然后退出程序。

 让我们来试一试： 

```python
# first_context_manager.py
import sys
class OpenFile(object):
    def __init__(self, path):
        self._path = path
        
    def __enter__(self):
        try:
        	self._f = open(self._path)
            return self._f
        except FileNotFoundError as _:
            print('get it and exit')
            sys.exit(1)
    
    def __exit__(self, exc_type, exc_value, exc_trace):
        if hasattr(self, '_f'):
        	self._f.close()  
            
# dong.txt doesn't exist!
with OpenFile('dong.txt') as f:
    f.readlines()    
```

上面我们定义了一个名为OpenFile的类， 在它的初始化方法中， 我们给对象挂载了文件路径， 在enter方法中， 我们使用open来尝试打开这个文件， 如果不存在就打印“get it and exit”。在exit方法中我们判断如果成功打开了文件， 则在退出的时候关闭这个文件。

将上面的代码保存为：first_context_manager.py，运行一下试试。

```shell
>>> python first_context_manager.py
>>> get it and exit
```

嗯，没问题。