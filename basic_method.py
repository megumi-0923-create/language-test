import csv
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup


#通过Unicode编码判断某个字符是否是某个语言的字符
def contains_lang_chars(lang_ranges,text,det_null=False):
    # 专业术语，不进行翻译的内容
    special_char = ['UI', 'API', 'STD', 'AI', 'HUD', 'NPC', 'Int', 'Bool', 'Enum']
    char_li=True
    #将检测内容含有专业术语的部分去除
    for char in special_char:
        if char in text:
            text=text.replace(char,'')
    if det_null:
        if text.strip() == '':
            char_li = False
    spe_char=[(0x020, 0x039),(0x05B, 0x05D)]
    for char in text.strip():
        found = False
        code = ord(char)  # 获取一个字符的 Unicode 码值（十进制）
        # 检查这个码值是否没有落在泰语区段内
        for start, end in lang_ranges:
            if start<=code<=end:
                found = True
                break
        for start_spechar, end_spechar in spe_char:
            if start_spechar<=code<=end_spechar:
                found = True
                break
        if not found:
            return False
    if not char_li:
        return False
    return True

#将测试结果写入 测试结果.csv文件
def write_result(element_txt,element,result):
    file= "测试结果_th.csv"
    with open(file,"a",newline="",encoding="utf-8") as f:
        fieldnames = ['element_txt', 'element', 'result']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        # 写入数据行
        if result:
            a="pass"
        elif result=='':
            a=''
        else:
            a='fail'
        writer.writerow({'element_txt': element_txt, 'element': element, 'result': a})

#打印方法名
def test_print_name_th(method):
    def wrapper(*args, **kwargs):
        # 这里可以打印测试方法名
        with open('测试结果_th.csv', 'a', newline='')as f:
            writer = csv.writer(f)
            writer.writerow({method.__qualname__})
        return method(*args, **kwargs)
    return wrapper

#找到元素后，检测字符
def det_lang_new(driver,xpath,lang_ranges):
    element = driver.find_element(By.XPATH,xpath)
    element_html = element.get_attribute("outerHTML")
    element_text = element.get_attribute('textContent')
    result = contains_lang_chars(lang_ranges, element_text)
    write_result(element_text,element_html,  result)

#
def get_th_text(html_element,label):
    # 创建BeautifulSoup解析对象
    soup = BeautifulSoup(html_element, 'html.parser')
    # 查找所有label标签
    tags = soup.find_all(label)
    # 提取每个label的文本内容（包含标签本身）
    list = []
    list_element = []
    for th in tags:
        list.append(th.get_text())
        list_element.append(th)
    return list, list_element