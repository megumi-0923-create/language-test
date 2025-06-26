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
driver.implicitly_wait(2)
driver.get("https://ffcraftland.garena.com/en/docs/api-1-24/")
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

with open('测试结果_th.csv', 'w') as f:
    pass
element = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/aside/div/div[4]/div/div/ul/li[1]/ul/li[1]/ul/li[1]/div/div/a')
element.click()
time.sleep(1)
html_element = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/section/nav').get_attribute(
    'outerHTML')
text, element_list = get_th_text(html_element, 'li')
for i, value in enumerate(text):
    if i % 2 == 1:
        continue
    result = contains_lang_chars(thai_ranges, value)
    write_result(value, element_list[i], result)
write_result('', '', '')
# 点击左侧列表后，检查
elements = driver.find_elements(By.XPATH,'//a[@class="transition-colors duration-300 hover:text-primary"][contains(@href, "/en/docs/api-")]')
print(elements)
for i, element in enumerate(elements):
    time.sleep(0.5)
    element_root = driver.find_element(By.XPATH, '//div[@class="inline-flex flex-wrap"]').get_attribute('outerHTML')
    element_root_middle = driver.find_element(By.XPATH, '//section[@class="app-docs-content"]').get_attribute('outerHTML')
    element_aside_index = driver.find_element(By.XPATH, '//div[@class="app-docs-nav-index"]')
    element_root_aside = driver.find_element(By.XPATH, '//aside[@class="app-docs-nav"]').get_attribute('outerHTML')
    print(element.get_attribute('outerHTML'))
    print(element.get_attribute('textContent'))
    if 'Obsolete' in element.get_attribute('textContent') or element.get_attribute('textContent') == '':
        continue
    url = element.get_attribute('href')
    pattern = '/en/docs/(.*)'
    match = re.search(pattern, url)
    result = match.group()
    print(result)
    element_new = driver.find_element(By.XPATH,f'//a[@class="transition-colors duration-300 hover:text-primary"][@href="{result}"]')
    element_new.click()
    # 检查被点击的左侧的二级分类下的选项
    elemnet_new_text = element_new.get_attribute('textContent')
    result = contains_lang_chars(thai_ranges, elemnet_new_text)
    write_result(elemnet_new_text, element_new.get_attribute('outerHTML'), result)
    # 检测导航栏
    html_element = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/section/nav').get_attribute(
        'outerHTML')
    text, element_list = get_th_text(html_element, 'li')
    for i, value in enumerate(text):
        if i % 2 == 1:
            continue
        result = contains_lang_chars(thai_ranges, value)
        write_result(value, element_list[i], result)
    # 检测h1标题(api标题和declaration)
    html_element = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/section').get_attribute(
        'outerHTML')
    text, element_list = get_th_text(html_element, 'h1')
    for i, value in enumerate(text):
        result = contains_lang_chars(thai_ranges, value)
        write_result(value, element_list[i], result)
    # 检测api的曾用名,没有曾用名就跳过
    try:
        html_element = driver.find_element(By.XPATH, '//div[@class="gfr-dropdown-wrapper z-20"]').get_attribute(
            'outerHTML')
        text, element_list = get_th_text(html_element, 'li')
        text_used_name, element_list_used_name = get_th_text(html_element, 'span')
        for i, value in enumerate(text):
            result = contains_lang_chars(thai_ranges, value)
            write_result(value, element_list[i], result)
        for i, value in enumerate(text_used_name):
            result = contains_lang_chars(thai_ranges, value)
            write_result(value, element_list_used_name[i], result)
    except:
        pass

    # 检查标题底下，所属二级目录/客户端，移动端/支持pc或移动端
    text, element_list = get_th_text(element_root, 'div')
    for i, value in enumerate(text):
        result = contains_lang_chars(thai_ranges, value)
        write_result(value, element_list[i], result)

    write_result('','','')
    text, element_list = get_th_text(element_root, 'a')
    for i, value in enumerate(text):
        result = contains_lang_chars(thai_ranges, value)
        write_result(value, element_list[i], result)

    text, element_list = get_th_text(html_element, 'p')
    write_result('','','')
    for i, value in enumerate(text):
        result = contains_lang_chars(thai_ranges, value)
        write_result(value, element_list[i], result)
    write_result('','','')
    try:
        elements_api=driver.find_elements(By.CLASS_NAME,'blocklyText')
        for element in elements_api:
            element_html_api=element.get_attribute('outerHTML')
            element_text_api=element.get_attribute('textContent')
            result=contains_lang_chars(thai_ranges,element_text_api)
            write_result(element_text_api, element_html_api, result)
            print(element_text_api)
        text_h2,element_list_h2 = get_th_text(element_root_middle, 'h2')
        print(text_h2)
        for index, value in enumerate(text_h2):
            result = contains_lang_chars(thai_ranges, value)
            print(value)
            write_result(value, element_list_h2[index], result)
        element_root_footer = driver.find_element(By.XPATH,'//footer[@class="flex justify-between h-7 max-lg:h-9"]').get_attribute('outerHTML')
        a = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/section/section[3]/footer/a[2]/span[1]')
        # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__nuxt"]/section/main/section/div/section/section/section/section[3]/footer/a[2]/span[1]')))
        if not a.is_displayed():
            print('111111')
        print('--------')
        print(a.get_attribute('textContent'))
        text_h2, element_list_h2 = get_th_text(element_root_footer, 'span')
        print(text_h2)
        print('---------')
        a, b = get_th_text(element_root_aside, 'a')
        print(a)
        print('>>>>>>>>>>')
        print(element_aside_index.get_attribute('textContent'))
        print('///////////')
    except:
        pass
    write_result('', '', '')
    print('======')

