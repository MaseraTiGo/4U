# -*- coding: utf-8 -*-
# @File    : pretty_coze
# @Project : 4U
# @Time    : 2024/6/4 14:28
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import pygments
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter


def display_pretty_code(filename, language):
    # 读取文件内容
    with open(filename, 'r') as file:
        code = file.read()

    # 获取对应语言的lexer
    lexer = get_lexer_by_name(language)

    # 使用TerminalFormatter进行终端输出格式化
    formatter = TerminalFormatter()

    # 高亮代码
    pretty_code = highlight(code, lexer, formatter)

    # 打印高亮后的代码
    print(pretty_code)


if __name__ == "__main__":
    # 示例：显示一个Python文件的美化代码
    display_pretty_code('__init__.py', 'python')
