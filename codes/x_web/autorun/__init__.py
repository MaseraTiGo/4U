# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : ez_web
# @Time    : 2023/9/11 16:18
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
if __name__ == '__main__':

    import pyotp

    # 1. 生成一个基于时间的一次性密码的密钥 (通常你会保存这个密钥)
    secret = pyotp.random_base32()
    print(f"密钥: {secret}|{len(secret)}")

    # 2. 创建一个 TOTP 对象
    totp = pyotp.TOTP(secret)

    # 3. 生成当前时间的动态口令
    current_otp = totp.now()
    print(f"当前动态口令: {current_otp}")

    # 4. 验证动态口令
    input_otp = input("请输入动态口令: ")
    if totp.verify(input_otp):
        print("动态口令验证成功！")
    else:
        print("动态口令验证失败。")
