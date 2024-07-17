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
import base64

from gmssl import sm2, func


def verify_keys(data: str = "fuck you".encode()):
    # 待加密数据
    data = b"u=operator&p=ADmin@123&t=1721198961"

    # 加密（只需公钥）
    sm2_crypt_enc = sm2.CryptSM2(public_key=public_key, private_key=None)
    enc_data = sm2_crypt_enc.encrypt(data)
    enc_data_str = base64.b64encode(enc_data).decode('utf-8')
    print("Encrypted data:", enc_data_str)
    # enc_data = b'\xf1\x0fN-3\x15\xf8;\xc5\x85\xf8\x89\xe9;v\x8d\x98~\xd9\xd8\xb7\xcd\xdd\xfc/y\xcb+\x9f\xa5\xa9\xdd\xcc\xd0\xf5\x0e\xaf\xe3\xfd\xf1\x9c\x90\x9c\x14\x12ds"N\xb3\x91\xc5\xa3\xf6\x19Vx\xa2\xce\xcb\x0b\xd8\x97\xbf\x0bA\x1dm,G\xc5\xe2\xa4\x9c}`\t\xb6\xa2\x06\xcd\xe5`cR\xe3\xf6e\x14q@\xac\xe5\xd1!\xb1\r\x98V\xcfS\x96\xe4\xe7\x04\xe7\t\xf2\xfbk\xc8\xb2S\xf1Y@k\xb8{\x1cCY\x8fa\t\xe6\x86\xae(p\xe1'

    # 解密（只需私钥）
    sm2_crypt_dec = sm2.CryptSM2(public_key=public_key, private_key=private_key)
    enc_data_b = base64.b64decode(enc_data_str)
    dec_data = sm2_crypt_dec.decrypt(enc_data_b)
    print("Decrypted data:", dec_data.decode('utf-8'))



def gen_keys():
    global private_key, public_key
    private_key = func.random_hex(128)
    sm2_crypt = sm2.CryptSM2(private_key=private_key, public_key='')
    public_key = sm2_crypt._kg(int(private_key, 16), sm2.default_ecc_table['g'])

    print("Private key:", private_key)
    print("Public key:", public_key)


if __name__ == '__main__':
    private_key = "eb09c0eceb4fcc8e1a9dcbb87a06bae84df5e37a7c4e1ae169d980bd1ac2f587dc24533a9bd61d852e001c47d6c96234550d06f9dcb792f4b3f3d62a433ea571"
    public_key = "2443f3a32beaecbd203e0960528451319dec220de76298f16451da184e7076ea55666ec757e0c4685925ad9f50b54d678e387cb991c7d8d6fe967fc3887a3c89"
    # gen_keys()
    verify_keys()
