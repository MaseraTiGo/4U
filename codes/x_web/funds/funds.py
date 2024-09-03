# -*- coding: utf-8 -*-
# @File    : funds
# @Project : x_web
# @Time    : 2024/1/16 16:44
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import requests


class Founds:
    BaseUrl = 'http://192.168.203.53:3000/fundMNHisNetList?FCODE={fcode}&pageIndex=1&pagesize=1'

    @classmethod
    def get_funds(cls, fund_code):
        try:
            ret = requests.get(cls.BaseUrl.format(fcode=fund_code)).json()
            networth = float(ret['Datas'][0]['DWJZ'])
        except Exception as e:
            networth = 0.0
            print(f"dong ---------------> get found: {fund_code} error: {e}")
        else:
            print(
                f"dong ---------------> get found: {fund_code} success, networth is: {networth}")
        return networth


if __name__ == '__main__':
    Founds.get_funds('007744')
