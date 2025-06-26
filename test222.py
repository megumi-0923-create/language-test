import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from basic_method import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get("https://ffcraftland.garena.com/en/docs/type-316/")
driver.maximize_window()

html_element = driver.find_element(By.XPATH,'//a[@href="/en/docs/api/"][@class="transition-colors duration-300 hover:text-primary"]')
html_element.click()
time.sleep(20)