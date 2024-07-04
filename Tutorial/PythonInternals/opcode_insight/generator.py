# -*- coding: utf-8 -*-
# @File    : generator
# @Project : 4U
# @Time    : 2024/6/25 14:15
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import dis

"""
 17           0 RETURN_GENERATOR
              2 POP_TOP
              4 RESUME                   0

 18           6 LOAD_GLOBAL              1 (NULL + range)
             18 LOAD_FAST                0 (i)
             20 PRECALL                  1
             24 CALL                     1
             34 GET_ITER
        >>   36 FOR_ITER                 6 (to 50)
             38 STORE_FAST               1 (_)

 19          40 LOAD_FAST                1 (_)
             42 YIELD_VALUE
             44 RESUME                   1
             46 POP_TOP
             48 JUMP_BACKWARD            7 (to 36)

 18     >>   50 LOAD_CONST               0 (None)
             52 RETURN_VALUE
"""


def generator_a(i):
    for _ in range(1, i, 3):
        yield _


dis.dis(generator_a)
