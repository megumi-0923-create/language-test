from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from basic_method import *
from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re

# U+0020  空格
# U+0021 ! 叹号
# U+0022 " 双引号
# U+0023 # 井号
# U+0024 $ 价钱／货币符号
# U+0025 % 百分比符号
# U+0026 & 英文“and”的简写符号
# U+0027 ' 引号
# U+0028 ( 开 圆括号
# U+0029 ) 关 圆括号
# U+002A * 星号
# U+002B + 加号
# U+002C , 逗号
# U+002D - 连字号／减号
# U+002E . 句号
# U+002F / 由右上至左下的斜线
# U+0030 0 数字 0
# U+0031 1 数字 1
# U+0032 2 数字 2
# U+0033 3 数字 3
# U+0034 4 数字 4
# U+0035 5 数字 5
# U+0036 6 数字 6
# U+0037 7 数字 7
# U+0038 8 数字 8
# U+0039 9 数字 9


driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.get("https://ffcraftland.garena.com/en/docs/")
driver.maximize_window()


thai_ranges = [
    (0xE00, 0xE7F),  # U+0E00~U+0E7F: Laic Type
    (0xE80, 0xEAF),  # U+0E80~U+0EAF: Tham Type
    (0xEB0, 0xED5),  # U+0EB0~U+0ED5: Thai Supplement
    # 可以根据需要增加其他扩展区段
]

# #
'''
elements=driver.find_elements(By.XPATH,'//a[@class="transition-colors duration-300 hover:text-primary"][contains(@href, "/en/docs/api-")]')

for i,element in enumerate(elements):
    time.sleep(1)
    print(element.get_attribute('outerHTML'))
    print(element.get_attribute('textContent'))
    if 'Obsolete' in element.get_attribute('textContent'):
        continue
    url=element.get_attribute('href')
    pattern='/en/docs/(.*)'
    match=re.search(pattern,url)
    result=match.group()
    print(result)
    element_new=driver.find_element(By.XPATH,f'//a[@class="transition-colors duration-300 hover:text-primary"][@href="{result}"]')
    element_new.click()
    print('======')
'''
time.sleep(1)
# WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'')))
element_module_tab=driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/aside/div/div[2]/div[1]/span')
element_module_tab.click()
for i in range(40):
    element = driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/div/aside/div/div[4]/div/div/ul/li[{i + 1}]/div/div/a')
    element.click()
    time.sleep(0.5)
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/section/section[1]/h1')))
    module_middle_root=driver.find_element(By.XPATH,'//section[@class="app-docs-content"]').get_attribute('outerHTML')
    module_aside_root=driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/aside/div').get_attribute('outerHTML')
    text_a,element_a=get_th_text(module_middle_root,'a')
    print(text_a)
    text_h1, element_h1 = get_th_text(module_middle_root, 'h1')
    print(text_h1)
    text_span, element_span = get_th_text(module_middle_root, 'span')
    print(text_span)
    text_th, element_th = get_th_text(module_middle_root, 'th')
    print(text_th)
    text_td, element_td = get_th_text(module_middle_root, 'td')
    print(text_td)
    element_required_tips=driver.find_element(By.XPATH,'//div[@class="gfr-tooltip-content max-w-60 text-center"]')
    print(element_required_tips.get_attribute('textContent'))
    text_aside_a,element_aside_a=get_th_text(module_aside_root,'a')
    print(text_aside_a)
    element_aside_index=driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/aside/div/div[1]')
    print(element_aside_index.get_attribute('textContent'))
    print('================')
