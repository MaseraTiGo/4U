# -*- coding: utf-8 -*-
# @File    : pos_only
# @Project : 4U
# @Time    : 2024/6/17 14:43
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from gmssl import sm2, func


def verify_keys(data: str = "fuck you".encode()):
    # 待加密数据
    data = b"Hello, SM2 Encryption!"

    # 加密（只需公钥）
    sm2_crypt_enc = sm2.CryptSM2(public_key=public_key, private_key=None)
    enc_data = sm2_crypt_enc.encrypt(data)
    print("Encrypted data:", enc_data)

    # 解密（只需私钥）
    sm2_crypt_dec = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    dec_data = sm2_crypt_dec.decrypt(enc_data)
    print("Decrypted data:", dec_data.decode('utf-8'))



def gen_keys():
    global private_key, public_key
    private_key = func.random_hex(64)
    sm2_crypt = sm2.CryptSM2(private_key=private_key, public_key='')
    public_key = sm2_crypt._kg(int(private_key, 16), sm2.default_ecc_table['g'])

    print("Private key:", private_key)
    print("Public key:", public_key)


if __name__ == '__main__':
    private_key = None
    public_key = None
    gen_keys()
    verify_keys()
