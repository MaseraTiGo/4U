# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : x_web
# @Time    : 2023/1/13 10:42
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import re
import time

import PyPDF2
from PyPDF2 import PageObject
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

repo = []
fail_words = []
p_word = re.compile('(\w+)\[')
p_subject = re.compile('(.+)?[\u4e00-\u9fa5]+')


def get_page_lines(page: PageObject, p):
    lines = page.extract_text().split('\n')
    for line in lines:
        ret = p_word.search(line)
        if ret:
            cur_word = ret.groups()[0]
            if cur_word not in repo:
                repo.append(cur_word + '\n')


def get_all_toefl_words_from_pdf(pdf: str = "TOEFL.pdf", p_p=p_subject, start=0, end=-1):
    reader = PyPDF2.PdfReader(pdf)
    for page in reader.pages[start:end]:
        get_page_lines(page, p_p)


def write_2_csv(csv: str = "TOEFL_subjects.txt"):
    with open(csv, 'w') as shit:
        shit.writelines(repo)


get_all_toefl_words_from_pdf(start=181, end=183)
print(len(repo))
print(repo)
# write_2_csv()


# def get_chrome_driver(wait=10):
#     driver = webdriver.Chrome()
#     driver.get('https://www.youdao.com/result?word=%20&lang=en')
#     time.sleep(wait)
#     driver.minimize_window()
#     return driver
#
#
# def search_and_collect_word(word: str, driver):
#     input_ele.send_keys(Keys.CONTROL, 'a')
#     input_ele.send_keys(word)
#
#     search_ele.click()
#
#     try:
#         title_ele = WebDriverWait(driver, timeout=0.5).until(
#             lambda d: d.find_element(By.CLASS_NAME, f'title'))
#         a_eles = title_ele.find_elements(By.XPATH, './div/a')
#         for a_ele in a_eles:
#             class_name = a_ele.get_attribute('class')
#             if class_name == 'word-operate add':
#                 a_ele.click()
#                 break
#             if class_name == 'word-operate add added':
#                 print(f"dong ---------> added: {word}")
#                 break
#         else:
#             fail_words.append(word + '\n')
#     except Exception as _:
#         fail_words.append(word + '\n')
#
#
# if __name__ == '__main__':
#     # driver = get_chrome_driver()
#     # s_time = time.time()
#     # input_ele = driver.find_element(By.XPATH, '//*[@id="search_input"]')
#     # search_ele = driver.find_element(By.XPATH,
#     #                                  '//*[@id="searchLayout"]/div/header/div/div/div/div/div/a')
#     # with open('TOEFL_2.txt') as shit:
#     #     for m_line in shit.readlines():
#     #         word = m_line.strip('\n')
#     #         print(f"dong -----------> current word: {word}")
#     #         try:
#     #             search_and_collect_word(word, driver)
#     #         except Exception as e:
#     #             fail_words.append(word + '\n')
#     #             print(f"dong -------------> fail word: {word}")
#     #
#     # with open('fail.txt', 'w') as shit:
#     #     shit.writelines(fail_words)
#     #
#     # e_time = time.time()
#     # print(f"dong --------------> all cost: {e_time - s_time}")