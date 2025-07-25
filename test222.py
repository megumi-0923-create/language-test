import re
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from basic_method import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get("https://ffcraftland.garena.com/en/docs/event-1-175/")
driver.maximize_window()

file_path='UGCBlockConfig.csv'
df = pd.read_csv(file_path,encoding='utf-8')

# 指定查找条件和目标字段
search_value = '18'          # 要查找的特定值
search_column = 'id'    # 包含目标值的列名
target_column = 'Division'    # 要获取值的列名

time.sleep(2)
element_root_owner = driver.find_element(By.XPATH,'//div[@class="flex w-full justify-start py-2"]').get_attribute('outerHTML')
text_owner,element_list_owner = get_th_text(element_root_owner, 'a')
for index, value in enumerate(text_owner):
    print(value)
print('------')
text_owner, element_list_owner = get_th_text(element_root_owner, 'span')
for index, value in enumerate(text_owner):
    print(value)
time.sleep(1000)
