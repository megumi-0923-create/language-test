import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from basic_method import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get("https://ffcraftland.garena.com/en/docs/api/")
driver.maximize_window()

file_path='UGCBlockConfig.csv'
df = pd.read_csv(file_path,encoding='utf-8')

# 指定查找条件和目标字段
search_value = '18'          # 要查找的特定值
search_column = 'id'    # 包含目标值的列名
target_column = 'Division'    # 要获取值的列名

time.sleep(2)
driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[4]/div/div/a').click()
result_url = '/en/docs/api-1-25/'

element_new = driver.find_element(By.XPATH,f'//a[@href="{result_url}"]')
element_new.click()
time.sleep(10)
