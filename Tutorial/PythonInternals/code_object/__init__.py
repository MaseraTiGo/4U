# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : 4U
# @Time    : 2024/6/25 14:33
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

source_code = '''
def add(x, y):
    return x + y
'''

compiled_code = compile(source_code, '<string>', 'exec')
print(dir(compiled_code))

