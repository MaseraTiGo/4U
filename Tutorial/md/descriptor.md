## Python描述符漫漫游



```l
当时我醉美人家， 美人颜色如娇花

今日美人弃我去， 青楼珠箔天之涯

天涯娟娟姮娥月， 三五二八盈又缺

翠眉蝉鬓生别离， 一望不见心断绝

心断绝，几千里？

梦中醉卧巫山云， 觉来泪滴湘江水

湘江两岸花木深， 美人不见愁人心

含愁更奏绿绮琴， 调高弦绝无知音

美人兮美人， 不知为暮雨兮为朝云

相思一夜梅花发， 忽到窗前疑是君
```



#### 一个强行举的🌰

平日里的工作中，与数据打交道是一个绕不开的东西，检查数据有效性更是一个日常任务。一般是怎么做呢？常见的便是如此这般：

例如我们要检查个人信息的有效性(为了简便，此处只是简单的检查一下名字是否只有字母组成，年龄在0-120之间)：

```python
class Person:
    def __init__(self, name, age):
        if self.is_name_valid(name):
            self.name = name
        else:
            raise Exception('unvalid name')
        if self.is_age_valid(age):
            self.age = age
        else:
            raise Exception('unvalid age')
    
    
    @staticmethod
    def is_name_valid(name: str) -> bool:
        if not isinstance(name, str):
            return False
        if name.isalpha():
            return True
        return False
    
    @staticmethod
    def is_age_valid(age: int) -> bool:
        if not isinstance(age, int):
            return False
        if 0 <= age <= 120:
            return True
        return False
        
```







