# -*- coding: utf-8 -*-
# @File    : 0001_test
# @Project : x_web
# @Time    : 2023/2/15 17:37
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import asyncio
import time


async def inner(id_):

    print(id_)


async def say_after(delay, what, task=None):
    print(f"dong ------------->delay: {delay}")
    if task:
        task.cancel()
    print(f"dong ------------->delay: {delay}")
    await asyncio.shield(inner(delay))
    await asyncio.sleep(delay)
    print(what)


async def main():
    task1 = asyncio.create_task(
        say_after(5, 'hello'))

    task2 = asyncio.create_task(
        say_after(3, 'world', task=task1))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    # await task1
    # await task2
    ret = await asyncio.gather(asyncio.shield(task1), task2, return_exceptions=True)

    print(f"finished at {time.strftime('%X')}: {ret}")


asyncio.run(main())
