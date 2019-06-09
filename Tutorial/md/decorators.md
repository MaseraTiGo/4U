### Python装饰器入门

#### 目录

- [函数](#函数)

  - [一级对象](#一级对象)
  - [内部函数](#内部函数)
  
  - [把函数作为返回值](#把函数作为返回值)
- [简单的装饰器](#简单的装饰器)
  - [语法糖](#语法糖)
  - [带参数的装饰器](#带参数的装饰器)
  - [从装饰器中返回值](#从装饰器中返回值)
- [练练手](#练练手)
  - [参数校验](#参数校验)
  - [缓存结果](#缓存结果)
  - [插件注册](#插件注册)
- [高级一点的装饰器](#高级一点的装饰器)
  - [装饰类](#装饰类)
  - [类装饰器](#类装饰器)
  - [多层装饰器](#多层装饰器)
  - [带参数的装饰器](#带参数的装饰器)
- [总结](#总结)



#### 函数

#### 一级对象

我们知道在python中一切皆为对象， 而函数是一级对象， 有称为‘第一类对象’(first-class object)。这意味着函数可以像其他如字符串(str)、列表(list)等对象一样作为参数一样传递。例如下面这个列子：

```python
def people(name: str):
    return f'{name}, Gnt!'

def say_good_night(func):
    return func('Johnathan')

say_good_night(people)

>>>'Johnathan, Gnt!'
    
```

我们定义了两个函数people和say_good_night，然后将people这个函数作为了一个参数传给了say_good_night。



#### 内部函数

通常我们的函数都是定义在模块或者类中。不过， 在函数内部我们也是可以定义函数的，此时这个函数就称为‘内部函数’。（想一想， 类可不可以呢？自己试一试。）

看个小例子：

```python
def outter():
    print('I am in func of "outter"')
    def inner():
        print('I am in func of "inner"')

```

当我们调用outter()的时候， 输出会是什么呢？不放想一下。

```python
>>>outter()
>>>I am in func of "outter"
```

为什么I am in func of "inner"没有输出呢？

原因在于此时inner就相当于一个outter的一个局部变量。它直到outter被调用的时候才会被‘定义’。如果你尝试在outter外部调用它， 它会报inner未定义的错误，如下：

```python
>>>inner()
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-18-bc10f1654870> in <module>()
----> 1 inner()

NameError: name 'inner' is not defined
```

那么， 怎么才能使用inner呢？没错， 作为一个局部变量， 它只能在outter内部使用， 你可以试试在outter内部写上:inner()。

#### 把函数作为返回值

在上面我们讲过， 函数可以作为参数值传递， 你肯定也想到了它可以作为返回值返回。是的， 它确实可以！看下面这个例子：

```python
def operator():
	def add(x, y):
        return x + y
    return add
```

这个例子中我们定义了一个函数operator， 然后定义了一个内部函数add。operator返回函数add，add函数返回传入参数的和，下面我们尝试运行一下：

```python
In [23]: func = operator()
In [24]: func(5, 5)
Out[24]: 10
```

如我们期望的那样，5 + 5 =10。

同时我们查看一下func

```python
In [25]: func
Out[25]: <function __main__.operator.<locals>.add(x, y)>
```

它就是operator函数的内部add。

至此， 我们已经讲完了装饰器所需的基础， 下面正式开始装饰器之旅把。



#### 简单的装饰器

现在我们有一个函数， 它从1一直加到10,000， 我们来统计一下它所花费的时间。

```python
import time
def time_cost(func):
    def wrapper_time_cost():
        s = time.perf_counter()
        result = func()
        c = time.perf_counter() - s
        print(f'time costs: {c}, the result is:     {result}')
    return wrapper_time_cost

def count_num(num=10_000):    
	return sum((i for i in range(1, 10_1000 + 1)))

count_num = time_cost(count_num)
```

上面的代码我们做了什么呢？

我们将count_num函数作为参数传给了time_cost， 在time_cost

的内部函数中， 我们调用了count_num的引用func，并计算了时间。最后返回了内部函数wrapper_time_cost的引用。

我们运行一下试试：

```python
In [37]: count_num()
time costs: 0.007390180999664153, the result is: 5100550500
```

这就是我们所说的“装饰”， 本例中我们给count_num函数“装了”一个时间统计功能，但是并没有修改count_num函数中的代码。

这个时候我们思考一下， 此时的count_num打印出来会是谁的引用呢？有了前面的知识， 你肯定很快就能想到，它指向了time_cost的内部函数wrapper_time_cost，没错，事实如此。

```python
count_num
Out[38]: <function __main__.time_cost.<locals>.wrapper_time_cost()>
```

但是， 这有一个问题， 如果我们想知道count_num本来的样子有没有办法呢？

当然有！而且不需要太多操作。

我们只需要稍微修改即可。

```python
...
from functools import wraps # here
def time_cost(func):
    def wrapper_time_cost():
        ...
    return wraps(func)(wrapper_time_cost) # here
...
```

其实就是导入了一个wraps函数， 然后对我们内部函数‘装饰’了一遍。看看效果：

```python
In [41]: count_num
Out[41]: <function __main__.count_num(num=10000)>
```

嗯， 还不错不是么？

现在是不是对装饰器有一个相对的了解了？

简单点来说： 装饰器就是在不修改一个函数情况下，为它增加新的属性或功能。

或者换句话说：装饰器包装一个函数， 并改变它的行为。



#### 语法糖

英文原文‘syntactic sugar’， 中文译作‘语法糖’。很直观， 也很合适， 因为熟悉了以后， 它真的很甜。

上面尽管我们已经实现了装饰， 但是多多少少看上去差了那么些味道， 少了些‘甜味’， 哈哈， 强行解释一波。不过确实如此， 假如我们要为多个函数加上上面写的计时器。每个那么写一遍，总觉得不是那么回事且笨拙。

 于是乎语法糖就应运而生。让我们可以用一种简单的方式来实现。‘@’， 对，只需要在需要装饰的函数上面加上这个符号并跟上对应的函数。还是使用上面的例子， 做对应的修改。

```python
import time
from functools import wraps
def time_cost(func):
    @wraps(func)
    def wrapper_time_cost():
        s = time.perf_counter()
        result = func()
        c = time.perf_counter() - s
        print(f'time costs: {c}, the result is:     {result}')
    return wrapper_time_cost
@time_cost
def count_num(num=10_000):    
    return sum((i for i in range(1, 10_1000 + 1)))
```

如此一来， 我们运行count_num 不再需要那么繁琐了， 简单的直接调用就可以了：

```python
In [44]: count_num()
time costs: 0.007472928000424872, the result is:     5100550500

In [45]: count_num
Out[45]: <function __main__.count_num(num=10000)>
```

结果与之前无二。

如果你有其他的函数需要计时， 只需在你的函数前面加上@time_cost即可， 这也实现装饰器复用。



#### 带参数的装饰器

上面的例子中，我们的count_num函数实际上是接受了一个参数的，只是我们给了一个默认值，现在我们想要计算1到20,000的和， 如果我们传入20,000结果会是我们想要的么？不放试一下：

```python

In [26]: count_num(20_000)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-26-d8a41d05f67f> in <module>()
----> 1 count_num(20_000)

TypeError: wrapper_time_cost() takes 0 positional arguments but 1 was given
```

很不幸， 报错了， 它说wrapper_time_cost这个函数不需要参数，但是我们传进去了一个。

问题很明朗了：我们就让它接受一个参数不就可以了么？来试试吧。其它不动， 我们给wrapper_time_cost增加一个参数，向下面这样：

```python
def wrapper_time_cost(num):
    ...
    result = func(num)
    ...
```

再来试试， 看看结果如何：

```python
In [28]: count_num(20_000)
time costs: 0.00742289499976323, the result is:     5100550500
```

成功了！

但是，对，但是出现了， 前面我们说到装饰器可以复用， 但是这个可以么？假如我们还有一个say_hi的函数， 它接受两个参数， 我们还能用这个计时装饰器来计时么？

```python
@time_cost
def say_hi(src_name, to_name):
    print(f'{src_name} say hi to {to_name}')

say_hi('tom', 'anny')
```

再次报错：

```python
TypeError: wrapper_time_cost() takes 1 positional argument but 2 were given
```

错误很明显， 参数个数不对。在实际开发中， 我们的不同的函数接受的参数必定不同，如果这样写，肯定是满足不了复用的，这个时候就该*args， **kwargs上场了。

*args用于接收不定长的位置参数。

**kwargs用于接收不定长的关键字参数。

这似乎可以解决上诉问题了， 老样子， 用代码说话。

```python
def wrapper_time_cost(*args, **kwargs):
    ...
    result = func(*args, **kwargs)
    ...
# run
count_num(20_000)
say_hi('tom', 'anny')
```

结果如期， 没毛病。

```python

In [33]: count_num(20_000)
time costs: 0.007542204999936075, the result is:     5100550500

In [34]: say_hi('tom', 'anny')
tom say hi to anny
time costs: 0.00018185200042353244, the result is:     None
# 结果是None是因为在say_hi这个函数中，我们没有返回任何东西
```



#### 从装饰器中返回值

在上面的例子中， 你可能一经发现， 我们只是打印出了被装饰函数的返回值， 我们如果要接收这个值该怎么做呢？

return, 对， 就是这么简单。

让我们在装饰器内部函数里加上return。

```python
def wrapper_time_cost(*args, **kwargs):
        s = time.perf_counter()
        result = func(*args, **kwargs)
        c = time.perf_counter() - s
        print(f'time costs: {c}, the result is:     {result}')
        return result
# run count_num
res = count_num(50_000)
print(f'res is: {res}')

# output---------------------
In [36]: res = count_num(50_000)
time costs: 0.007627519000379834, the result is:     5100550500

In [37]: print(f'res is: {res}')
res is: 5100550500
```



#### 练练手

目前， 装饰器我们已经了解的差不多了， 是时候来几个有用的列子练练手了。



#### 参数校验

现在假如我们有两个函数， add和multi分别打印两个正整数相加和相乘的结果。我们不知道用户会传入多少参数、什么样的参数， 为了程序正常执行不报错， 我们需要对参数进行校验， 装饰器可以很好的胜任这个工作。来看下面的代码：

```python
def args_check(func):
    def wrapper_args_check(*args, **kwargs):
        if len(args) != 2:
            print('args num error, we need two, get %d' %len(args))
        else:
            a, b = args
            if isinstance(a, int) and isinstance(b, int):
                func(*args)
    return wrapper_args_check

@args_check
def add(x, y):
    print(x + y)
    
@args_check
def multi(x, y):
    print(x * y)

# output--------------------------------
add(3)
args num error, we need two, get 1

multi(1, 2, 3)
args num error, we need two, get 3

add(3, 4)
7

multi(3, 4)
12
```

还不错！



#### 缓存结果

现在我们写一个用于计算阶乘的函数。（这里涉及到函数递归， 如果有不清楚递归的请自行查阅）。

```python
def factorial(num):
    if num < 0:
        print('负数没有阶乘')
    elif num <= 1:
        return 1
    else:
    	return num * factorial(num - 1)
```

测试一下：

```python
factorial(8)

>>> 40320
```

没问题，但是有一点， 我们发现计算任意一个num， 我们都需要从1算到num，哪怕我们可能在此之前计算过num-1,这无疑是做了很多重复工作， 讲到这里， 你可能想到将算过的结果保存下来， 以备后用， 没错， 让我们用装饰器试试：

```python
def factorial_memcache(func):
    res_dict = {}
    def wrapper_factorial_memcache(num):
        if num in res_dict:
            return res_dict[num]
        else:
            wrapper_factorial_memcache.calls += 1
            res = func(num)
            res_dict[num] = res
            return res
    wrapper_factorial_memcache.calls = 0
    return wrapper_factorial_memcache

@factorial_memcache
def factorial(num):
    ...
            
```

在装饰器factorial_memcache中， 我们增加了一个名为res_dcit的字典， 用于存贮计算过阶乘的值， 还给内部函数wrapper_factorial_memcache挂了一个calls属性用来统计func调用次数， 运行一下， 看看效果：

```python

In [104]: factorial(6)
Out[104]: 720

In [105]: factorial.calls
Out[105]: 6

In [106]: factorial.calls = 0

In [107]: factorial(8)
Out[107]: 40320

In [108]: factorial.calls
Out[108]: 2
```

完全符合预期！

题外话：你可能注意到了factorial.calls = 0， 思考一下为什么。

#### 插件注册

最后一个练手， 我们定义一个register装饰器， 让经过register装饰的函数都出现插件列表中。

```python
PLUGINS = []

def register(func):
    PLUGINS.append(func.__name__)
	return func

@register
def add():
    ...

@register
def multi():
    ...
    
```

这个地方我们写了一个特别简单的装饰器register，它实现的功能就是把被它装饰的函数的名称放到插件列表里。

```python
In [3]: PLUGINS
Out[3]: ['add', 'multi']
```

注册成功。额， 是不是感觉简单到有点令人发指......





#### 高级一点的装饰器

截止到现在， 相信大家已经对装饰器有一个足够清晰的认识与理解了， 也能写出一些满足自己需求的装饰器了。 但是， 还有更高级的或者说复杂点的特性值得我们去学习，以便更好地解决我们的需求。

下面就让我们深入一点吧。

#### 装饰类

前面我们所写的装饰器都是用作在一个普通的函数上的， 那么它类上可以不可以用装饰器呢？

试试便知。

```python
from random import randint

@time_cost
class Test(object):
    def lazy(self):
        time.sleep(randint(1, 5))
        print('woo...')

# output -------------------------------------

In [16]: t = Test()
time costs: 6.409999855350179e-07, the result is:     <__main__.Test object at 0x000001DD1D737B00>

In [17]: t.lazy
Out[17]: <bound method Test.lazy of <__main__.Test object at 0x000001DD1D737B00>>

In [18]: t.lazy()
woo...
```

这个例子我们定义了一个Test类， 它有一个实例方法lazy， 这个lazy方法随机sleep1-5 s，这里使用了之前的计时装饰器。

根据结果， 不难看出， 这个装饰器在类实例化的时候起作用了，也就是说， 类也是可以被装饰的。下面我们来写一个单例模式（简单点来说就是一个类只能实例化出一个实例）加深一下印象。

```python
def singleton(cls):
    cls._instance = None
    def wrapper_singleton(*args, **kwargs):
    	if not cls._instance:
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    return wrapper_singleton

@singleton
class A(object):
    ...
```

本例中， 我们定义了一个类A， 并实现了一个singleton的装饰器，逻辑很简单， 先给传入的类挂上一个\_instances属性并赋值None， 然后在内部函数中判断， 如果这个属性为None， 说明未实例化过， 那就实例化并赋值给\_instance属性然后返回， 不为None的话就直接返回， 从而保证了实例的唯一性。

你可能注意到传入的参数由func变成了cls， 这是因为我们装饰类的时候传入的是一个类。 依然写成func也不会有功能上的问题， 但是会让人感到困惑。cls是一个约定的写法。

我们来实例化一下这个类， 并比较是否确实是一个单例。

```python
In [3]: a = A()
In [4]: b = A()
In [5]: a is b
Out[5]: True
```

这里我们用的是is来比较， 它可以对比两个对象的引用是否一样。

装饰类还有一种方式是装饰类的方法。让我们用计时装饰器装饰本小结开始例子中的lazy方法吧！

```python
class Test(object):
    @time_cost
    def lazy(self):
        time.sleep(randint(1, 5))
        print('woo...')
```

```python
Test().lazy()

In [23]: Test().lazy()
woo...
time costs: 3.00124057000005, the result is:     None
```

看来， 它睡了3s不是么。

其实一些常用的装饰器已经内建在python中了， 如@classmethod、@staticmethod、@property这些都作用于类的函数。如感兴趣， 可自行查阅。



#### 类装饰器

我们前面写的装饰器都是基于函数的， 那么类可不可以作为装饰器呢？一起来尝试一下。

首先让我们再回顾一下装饰器是怎么工作的：它接收一个函数或者类， 然后在对传入的类或者函数进行处理，并返回一个新的对象或原对象（还记得我们那个register装饰器吧）。

好了， 让我开始吧。

```python
class FakeLog(object):
    def __init__(self, func):
        self.func = func
        self.fake_log()
        
    def fake_log(self):
        print('start--------------------')
        print(f'excuting func is: {self.func.__name__}')
        self.func()
        print('end----------------------')

@FakeLog
def run():
    print('I am running!')
```

当你在敲完上面的代码的时候会立马得到一下输出：

```python
start--------------------
excuting func is: run
I am running!
end----------------------
```

而且， 当你调用run()的时候，错误出现了：

```python
>>> run()
>>> TypeError: 'FakeLog' object is not callable
```

先思考一下为什么。

立马得到输出是因为， 当我们用类做装饰器的时候， 默认会调用\__init__方法进行初始化（实例化一个类的时候总是会如此），并返回一个实例。 在这个初始化函数中我们调用了fake_log，所以便立马有了上面那些信息。

至于调用run()的时候报错， 那是因为此时的run已经变成FakeLog的一个实例对象， 这个是无法调用的。

这虽然说明了类可以作为装饰器， 但结果并不是我们想要的。我们想要的是自行调用run()。

那么问题来了， 此时run是一个实例对象， 我们想要的是一个可调用的对象，怎么办呢？能不能把实例对象变成可调用对象呢？

是时候让\__call__出场了！

\__call__是一个魔法函数， 它能让一个类的实例变的可调用。

```python
class Test(object):
    def __call__(self, name: str):
        print(f'hello, {name}')

In [26]: t = Test()
# output----------------------------------
In [27]: t('Johnathan')
hello, Johnathan        
```

对开始的例子我们做一下更改：

```python
class FakeLog(object):
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        print('start--------------------')
        print(f'excuting func is: {self.func.__name__}')
        self.func()
        print('end----------------------')
@FakeLog
def run():
    print('I am running!')
```

代码敲完了， 并没有直接运行， 送了一口气......

这里我们把fake_log换成了\__call__并增加了参数（既然可调用，能接受参数自然是应该的吧）。

检验的时候到了，敲入run():

```python
In [23]: run()
start--------------------
excuting func is: run
I am running!
end----------------------
```

嗯哼， Done！

小结一下\__init__方法用来存储传入的引用和做一些必要的初始化工作， 而\_\_call\_\_方法让实例对象变得可调用， 功能和之前内部函数wrapper\_xxx一样。



#### 多层装饰器

讲了这么多， 我们所做的一直是给一个函数或者类添加单一的装饰器， 那么可不可以添加多个呢？答案很简单， 必须可以，结合我们开篇讲的那些知识， 很好理解。

那么我们就来试试吧。

```python
def fake_log(func):
    def wrapper_fake_log(*args, **kwargs):
        print('start--------------------')
        print(f'excuting func is: {func.__name__}')
        func(*args, **kwargs)
        print('end----------------------')
    return wrapper_fake_log

@fake_log
@time_cost
def count_num(num=10_000):
    ...
```

本例中， 我们写了一个伪日志记录装饰器， 它只是简单的打印开始与结束， 然后结合之前的计时装饰器和count_num函数， 来测试一下。

```python
In [8]: count_num()
start--------------------
excuting func is: wrapper_time_cost
time costs: 0.007424178000064785, the result is:     5100550500
end----------------------
```

毫无意外的正常。可以看到我还在fake_log中打印了一个执行函数的名字， 这个是为了了解当有多个装饰器的时候， 它们的执行顺序：依次往下。这个很好理解， 不再赘述。



#### 带参数的装饰器

上面讲了那么多， 但是我们所写的装饰器默认都是不带参数的， 实际上， 装饰器也是可以带上参数的。

这有什么用呢？

当然有用， 譬如我们有很多请求函数， 当失败后， 有些我们希望重新尝试两次， 有些三次等等， 这个时候参数就有了用处，。

这里我们只是介绍一下如何加参数， 就只写一个简单的例子。 

```python
def repeat(num_times):
	def decorator_repeat(func):
        def wrapper_decorator_repeat(*args, **kwargs):
            for _ in range(num_times):
                func(*args, **kwargs)
        return wrapper_decorator_repeat
    return decorator_repeat

@repeat(3)
def say_love():
    print('i love u')
```

我们给之前熟悉的装饰器又加了一层，用来接收参数。 原理还是一样。

运行一下：

```python
In [32]: say_love()
i love u
i love u
i love u
```



既然已经讲过类装饰器， 不放我们也改一改这个repeat。

先自己试试，在看下面的例子。

小提示， 我们在\_\_init\_\_中完成初始化工作。

```python
class Repeat(object):
    def __init__(self, num_times):
        self.num_times = num_times
    
    def __call__(self, func):
        def wrapper_repeat(*args, **kwargs):
            for _ in range(self.num_times):
                func(*args, **kwargs)
        return wrapper_repeat

@Repeat(4)
def say_hate():
    print('go , I do not hate u')
    
```

走一个：

```python
In [46]: say_hate()
go , I do not hate u
go , I do not hate u
go , I do not hate u
go , I do not hate u
```

简要的说一下， 当我们给say_hate加上@Repeat(4),它首先实例化出了一个Repeat对象， 我们且称为r，并给r的num_times赋值为4，然后执行r(say_hate)得到wrapper_repeat对象， 接着调用wrapper_repeat并将say_hate的参数传入（此处没有传参）。便有了上面的结果。



#### 总结

好了， 洋洋洒洒啰里啰嗦了这么多， 总算是要结束了， 篇幅较长， 可能对于初次接触的人员来说， 有那么点点不容易， 没事， 相信自己， 多看一看、写一写、思考思考， 终会发现其实也就是那么点事。



























