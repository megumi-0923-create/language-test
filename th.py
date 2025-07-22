import csv
from basic_method import *
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import unittest
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#检测泰语
thai_ranges = [
    (0xE00, 0xE7F),  # U+0E00~U+0E7F: Laic Type
    (0xE80, 0xEAF),  # U+0E80~U+0EAF: Tham Type
    (0xEB0, 0xED5),  # U+0EB0~U+0ED5: Thai Supplement
    # 可以根据需要增加其他扩展区段
]


# char_test="ประเภทริจิดบอดี้ ()"
# print(contains_lang_chars(thai_ranges, char_test))
driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get("https://ffcraftland.garena.com/th/docs/api")
driver.maximize_window()




class surface_lang_detect(unittest.TestCase):
    def setUp(self):
        print("========测试开始========")

    def tearDown(self):
        with open('测试结果_th.csv', 'a', newline='')as f:
            writer = csv.writer(f)
            writer.writerow({})
        print("========测试结束========")
    #测试页面上方home,tutorial等menu页
    @test_print_name_th
    def test_01top_menu(self):
        for i in range(4):
            element_menu = driver.find_elements(by=By.CSS_SELECTOR, value=".gfr-menu-link.gfr-menu-link-line")[i]
            element_html=element_menu.get_attribute("outerHTML")
            element_menu_text=element_menu.text
            result=contains_lang_chars(thai_ranges, element_menu_text)
            write_result(element_menu_text,element_html,result)
    #测试左侧modules，references等文字
    @test_print_name_th
    def test_02left_menu(self):
        element=driver.find_element(by=By.CLASS_NAME, value='app-docs-filter-input')
        element_html=element.get_attribute("outerHTML")
        element_text = element.get_attribute('placeholder')
        result = contains_lang_chars(thai_ranges, element_text)
        write_result(element_text,element_html,result)
        #检查Modules和References
        for i in range(-1,-3,-1):
            element = driver.find_elements(By.XPATH,'//div[@class="app-docs-tab"]/span')[i]
            element_html = element.get_attribute("outerHTML")
            element_text = element.text
            result = contains_lang_chars(thai_ranges, element_text)
            write_result(element_text,element_html,  result)
        time.sleep(2)
    #测试modules下所有分类
    @test_print_name_th
    def test_03left_modules(self):
        #点击Modules按钮
        driver.find_elements(By.XPATH,'//div[@class="app-docs-tab"]/span')[-2].click()
        #检查modules下的所有分类页签
        for i in range(40):
            element = driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[{i+1}]/div/div/a')
            element_html = element.get_attribute("outerHTML")
            element_text = element.get_attribute('innerText')
            result = contains_lang_chars(thai_ranges, element_text)
            write_result(element_text,element_html,  result)
            time.sleep(0.5)
    #测试references下所有分类
    @test_print_name_th
    def test_04left_references(self):
        #点击References按钮
        driver.find_elements(By.XPATH,'//div[@class="app-docs-tab"]/span')[-1].click()
        #依次点开所有一级分类，并检测一级分类(api,event,type)
        for i in range(4):
            if i<3:
                driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[{i+1}]/div/div').click()
            element = driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[{i+1}]/div/div/a')
            element_html = element.get_attribute("outerHTML")
            element_text = element.text
            result = contains_lang_chars(thai_ranges, element_text)
            write_result(element_text,element_html,  result)
        time.sleep(1)
        #依次点开所有二级分类，并检测二级分类
        for i in range(2):
            for j in range(35):
                if i==0 and j==27 or (i==1 and j==8) or (i==1 and j==14):
                    continue
                if i==1 and j==19:
                    break
                driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[{i+1}]/ul/li[{j+1}]/div/div/span').click()
                element = driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[{i+1}]/ul/li[{j+1}]/div/div/span')
                element_html = element.get_attribute("outerHTML")
                element_text = element.text
                result = contains_lang_chars(thai_ranges, element_text)
                write_result(element_text,element_html,  result)
        #检测aside，type下的所有分类
        element_aside_type=driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[3]/ul').get_attribute('outerHTML')
        text_aside_type,element_list_aside_type=get_th_text(element_aside_type,'a')
        for index,value in enumerate(text_aside_type):
            result = contains_lang_chars(thai_ranges, value)
            write_result(value,element_list_aside_type[index],  result)
        #检测aside下的 已废弃文章显示 按钮
        element_aside_obsole_button = driver.find_element(By.XPATH, "//label[@class='com-label cursor-pointer']")
        result=contains_lang_chars(thai_ranges,element_aside_obsole_button.get_attribute('textContent'))
        write_result(element_aside_obsole_button.get_attribute('textContent'),element_aside_obsole_button.get_attribute('outerHTML'), result)
        time.sleep(100000)

    # # 检查enum页，右边的index选项
    # @test_print_name_th
    # def test_05enum_index(self):
    #     #点击左侧enum页
    #     driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[4]/div/div/a').click()
    #     time.sleep(1)
    #     #检测index下的表格内容
    #     WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,'//aside[@class="app-docs-nav"]')))
    #     element_index=driver.find_element(By.XPATH,'//aside[@class="app-docs-nav"]').get_attribute('outerHTML')
    #     text_enum_index,element_list_enum_index=get_th_text(element_index,'a')
    #     for index, value in enumerate(text_enum_index):
    #         result = contains_lang_chars(thai_ranges, value)
    #         write_result(value, element_list_enum_index[index], result)
    #     #检测index本身
    #     element_index_self=driver.find_element(By.XPATH,'//div[@class="app-docs-nav-index"]')
    #     print(element_index_self.get_attribute('textContent'))
    #
    # #检查enum页，中间部分其余内容
    # @test_print_name_th
    # def test_06enum_rest(self):
    #     #点击左侧enum按键
    #     driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[4]/div/div/a').click()
    #     time.sleep(1)
    #     #references
    #     element_breadcrum_references=driver.find_element(By.XPATH, '//span[@class="breadcrumb-text"]')
    #     element_breadcrum_references_text=element_breadcrum_references.get_attribute('textContent')
    #     result=contains_lang_chars(thai_ranges, element_breadcrum_references_text)
    #     write_result(element_breadcrum_references_text,element_breadcrum_references.get_attribute('outerHTML'), result)
    #     #大标题enum
    #     element_h1_enum=driver.find_element(By.XPATH, '//h1[@class="gfr-title gfr-title-1 gfr-title-left app-docs-title"]')
    #     element_h1_enum_text=element_h1_enum.get_attribute('textContent')
    #     result=contains_lang_chars(thai_ranges, element_h1_enum_text)
    #     write_result(element_h1_enum_text,element_h1_enum.get_attribute('outerHTML'), result)
    #     #下方的其余内容
    #     '''
    #     0722
    #     '''
    #     element_html=driver.find_element(By.XPATH, '//article[@class="app-markdown-content"]').get_attribute("outerHTML")
    #     #检测标签中含有a的内容
    #     list,list_element=get_th_text(element_html,'a')
    #     for i in range(len(list)):
    #         result=contains_lang_chars(thai_ranges, list[i-1])
    #         write_result(list[i-1],list_element[i-1],  result)
    #     write_result('','','')
    #     # 检测标签中含有p的内容
    #     list, list_element = get_th_text(element_html, 'p')
    #     for i in range(len(list)):
    #         result = contains_lang_chars(thai_ranges, list[i - 1])
    #         write_result(list[i - 1],list_element[i - 1],  result)
    #     write_result('', '', '')
    #     #检测表格中的标题
    #     list, list_element = get_th_text(element_html, 'th')
    #     for i in range(len(list)):
    #         result = contains_lang_chars(thai_ranges, list[i - 1])
    #         write_result(list[i - 1],list_element[i - 1],  result)
    #     write_result('', '', '')
    #     #检测表格中的内容,第1列是key名字，第3列是脚本的名字，所以只检查第二列
    #     list, list_element = get_th_text(element_html, 'td')
    #     list_new,list_element_new=[],[]
    #     for i in range(len(list)):
    #         if i % 3 == 2:
    #             list_new.append(list[i - 1])
    #             list_element_new.append(list_element[i - 1])
    #     for i in range(len(list_new)):
    #         result = contains_lang_chars(thai_ranges, list_new[i - 1])
    #         write_result(list_new[i - 1],list_element_new[i - 1],  result)
    #     write_result('', '', '')
    #
    # #api部分
    # @test_print_name_th
    # def test_07nav(self):
    #
    #     '''
    #
    #     1111111111111111
    #     11111
    #     11111
    #     '''
    #     # with open('测试结果_th.csv', 'w') as f:
    #     #     pass
    #
    #     # element = driver.find_element(By.XPATH,'//a[@href="/th/docs/api/"][@class="transition-colors duration-300 hover:text-primary"]')
    #     # element.click()
    #     # time.sleep(1)
    #
    #     # 点击break loop
    #     '''
    #     0722
    #     '''
    #     print('test_07nav!!!!!!!!!!!!!')
    #     driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[1]/ul/li[1]/ul/li[1]/div/div/a').click()
    #     time.sleep(0.5)
    #     #上方导航
    #     WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,'//nav[@class="breadcrumb-container"]')))
    #     html_element = driver.find_element(By.XPATH,'//nav[@class="breadcrumb-container"]').get_attribute('outerHTML')
    #     print(html_element)
    #     text, element_list = get_th_text(html_element, 'li')
    #     for i,value in enumerate(text):
    #         if i%2==1:
    #             continue
    #         result=contains_lang_chars(thai_ranges, value)
    #         write_result(value, element_list[i], result)
    #     write_result('', '', '')
    #     #点击左侧列表后，检查
    #     elements = driver.find_elements(By.XPATH,'//a[@class="router-link-active router-link-exact-active"][contains(@href, "/th/docs/api-") or contains(@href, "/th/docs/event-") or contains(@href, "/th/docs/type-")]')
    #
    #     '''
    #     11111122222
    #     33333
    #     '''
    #     # elements=driver.find_elements(By.XPATH,'//a[@class="transition-colors duration-300 hover:text-primary"][contains(@href, "/th/docs/api-44-")or contains(@href, "/th/docs/type-10")]')
    #
    #     for i, element in enumerate(elements):
    #         print(element.get_attribute('outerHTML'))
    #         print(element.get_attribute('textContent'))
    #         if element.get_attribute('textContent')=='':
    #             continue
    #         url = element.get_attribute('href')
    #         pattern = '/th/docs/(.*)'
    #         match = re.search(pattern, url)
    #         result_url = match.group()
    #         #获取url中最后一位，这个数字是ugcblock表中，api的id，根据id，获得该api的division，用于判断该图元颜色是否正确
    #         id_division=result_url.split('/')[-2].split('-')[-1]
    #         print(result_url)
    #
    #         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,f'//a[@href="{result_url}"]')))
    #         print('<<<<<')
    #         element_new = driver.find_element(By.XPATH,f'//a[@href="{result_url}"]')
    #         element_new.click()
    #         time.sleep(2)
    #         # 整个中间页面的元素
    #         # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/section')))
    #         print('>>>>>>')
    #         element_root_middle = driver.find_element(By.XPATH, '//section[@class="app-docs-content"]').get_attribute('outerHTML')
    #         # 标题下方所属二级分类等那一行的元素
    #         # WebDriverWait(driver,60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/section/main/section/section/section/section/section[1]/section/div/div')))
    #         element_root = driver.find_element(By.XPATH, '//div[@class="inline-flex flex-wrap"]').get_attribute('outerHTML')
    #         try:
    #             # 页面右侧的导航栏，index
    #             element_aside_index = driver.find_element(By.XPATH, '//div[@class="app-docs-nav-index"]')
    #             # 页面右侧导航栏的元素
    #             element_root_aside = driver.find_element(By.XPATH, '//aside[@class="app-docs-nav"]').get_attribute('outerHTML')
    #         except:
    #             pass
    #
    #         #检查api和event下的declaration是否为空
    #         if 'api' in result_url or 'event' in result_url:
    #             try:
    #                 #显示等待 脚本declaration渲染完成
    #                 # WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/section/section[3]/article/div[1]/pre/code/span')))
    #                 element_declaration=driver.find_element(By.XPATH,'//span[@class="hljs-keyword"]')
    #                 #该脚本的h1标题
    #                 element_h1_text=driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/section/section[1]/h1').get_attribute('textContent')
    #                 #如果有该元素,检查该元素的文本属性是否为空
    #                 text_declaration=element_declaration.get_attribute('textContent')
    #                 if text_declaration.strip()=='':
    #                     result=False
    #                     write_result(element_h1_text, '该api/event有脚本元素，但脚本为空', result)
    #             except:
    #                 # 该脚本的h1标题
    #                 element_h1_text = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/section/section[1]/h1').get_attribute('textContent')
    #                 result = False
    #                 write_result(element_h1_text, '该api/event没有脚本元素', result)
    #             #点击中间declaration界面，切换pc端和手机端的按钮，切换至pc端显示
    #             element_pcmobile_switch_button = driver.find_element(By.XPATH,'//button[@class="gfr-button w-8 h-7 max-lg:h-10 max-lg:w-11"]').click()
    #             #通过元素获取中间图元的显示颜色后，和预期进行对比
    #             element_api_color = driver.find_element(By.CLASS_NAME, 'blocklyPathDark')
    #             result=(element_api_color.get_attribute('fill') == api_color(id_division))
    #             write_result(id_division, '测试api颜色是否正确', result)
    #             '''
    #             11111
    #             '''
    #             if not result:
    #                 print(result_url)
    #
    #         #检查被点击的左侧的二级分类下的选项
    #         element_new_new=driver.find_element(By.XPATH,f'//a[@class="transition-colors duration-300 hover:text-primary"][@href="{result_url}"]')
    #         elemnet_new_text=element_new_new.get_attribute('textContent')
    #         result=contains_lang_chars(thai_ranges, elemnet_new_text)
    #         write_result(elemnet_new_text, element_new.get_attribute('outerHTML'), result)
    #         #检测导航栏
    #         html_element = driver.find_element(By.XPATH,'//nav[@class="mb-3.5 ltr:max-lg:pl-18 rtl:max-lg:pr-18 max-lg:min-h-24 max-lg:pb-5 max-lg:mb-0 max-lg:flex max-lg:items-center"]').get_attribute('outerHTML')
    #         text, element_list = get_th_text(html_element, 'li')
    #         for i, value in enumerate(text):
    #             if i % 2 == 1:
    #                 continue
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list[i], result)
    #         #检测h1标题(api标题和declaration)
    #         # time.sleep(0.5)
    #         html_element = driver.find_element(By.XPATH,'//section[@class="flex-1 pt-30 lg:pt-20 max-lg:w-full"]').get_attribute('outerHTML')
    #         text, element_list = get_th_text(html_element, 'h1')
    #         for i, value in enumerate(text):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list[i], result)
    #         #检测api的曾用名,没有曾用名就跳过
    #         try:
    #             html_element_usedname = driver.find_element(By.XPATH, '//div[@class="gfr-dropdown-wrapper z-20"]').get_attribute('outerHTML')
    #             text, element_list = get_th_text(html_element_usedname, 'li')
    #             text_used_name, element_list_used_name = get_th_text(html_element_usedname, 'span')
    #             for i, value in enumerate(text):
    #                 result = contains_lang_chars(thai_ranges, value)
    #                 write_result(value, element_list[i], result)
    #             for i, value in enumerate(text_used_name):
    #                 result = contains_lang_chars(thai_ranges, value)
    #                 write_result(value, element_list_used_name[i], result)
    #         except :
    #             pass
    #
    #
    #
    #         #检查标题底下，所属二级目录/客户端，移动端/支持pc或移动端
    #         text, element_list = get_th_text(element_root, 'div')
    #         for i, value in enumerate(text):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list[i], result)
    #         text, element_list = get_th_text(element_root, 'a')
    #         for i, value in enumerate(text):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list[i], result)
    #         #检查api描述段落文字
    #         text, element_list = get_th_text(html_element, 'p')
    #         write_result('', '', '')
    #         for i, value in enumerate(text):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list[i], result)
    #         write_result('', '', '')
    #         try:
    #             # 检查api图元内部的文字
    #             elements_api = driver.find_elements(By.CLASS_NAME, 'blocklyText')
    #             for element_api in elements_api:
    #                 element_html_api = element_api.get_attribute('outerHTML')
    #                 element_text_api = element_api.get_attribute('textContent')
    #                 result = contains_lang_chars(thai_ranges, element_text_api)
    #                 write_result(element_text_api, element_html_api, result)
    #             #检查api底下的input或return字样
    #             text_h2, element_list_h2 = get_th_text(element_root_middle, 'h2')
    #             for index, value in enumerate(text_h2):
    #                 result = contains_lang_chars(thai_ranges, value)
    #                 write_result(value, element_list_h2[index], result)
    #             #检查api底下的input或return列表
    #             #标题
    #             text_th,element_list_th = get_th_text(element_root_middle, 'th')
    #             for index, value in enumerate(text_th):
    #                 result = contains_lang_chars(thai_ranges, value)
    #                 write_result(value, element_list_th[index], result)
    #             #内容
    #             text_td, element_list_td = get_th_text(element_root_middle, 'td')
    #             for index, value in enumerate(text_td):
    #                 result = contains_lang_chars(thai_ranges, value)
    #                 write_result(value, element_list_td[index], result)
    #             #检查底部跳转页面
    #             element_root_footer = driver.find_element(By.XPATH,'//footer[@class="flex justify-between h-7 max-lg:h-9"]').get_attribute('outerHTML')
    #             a = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/section/section[3]/footer/a[2]/span[1]')
    #             # WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/section/section[3]/footer/a[2]/span[1]')))
    #             text_footer, element_list_footer = get_th_text(element_root_footer, 'span')
    #             for index, value in enumerate(text_footer):
    #                 result = contains_lang_chars(thai_ranges, value)
    #                 write_result(value, element_list_footer[index], result)
    #             #检查导航栏下的每个分类
    #             text_nav_link, element_list_nav_link = get_th_text(element_root_aside, 'a')
    #             for index, value in enumerate(text_nav_link):
    #                 result = contains_lang_chars(thai_ranges, value)
    #                 write_result(value, element_list_nav_link[index], result)
    #             #检查导航栏的index
    #             result=contains_lang_chars(thai_ranges, element_aside_index.get_attribute('textContent'))
    #             write_result(element_aside_index.get_attribute('textContent'),element_aside_index.get_attribute('outerHTML'),result)
    #         except:
    #             pass
    #         #event下，有api的owner/type下，有combine的内容，2个用的是同一个class，需要单独检测
    #         if 'event' in result_url or 'type' in result_url:
    #             try:
    #                 element_root_owner = driver.find_element(By.XPATH,'//div[@class="flex w-full justify-start py-2"]').get_attribute('outerHTML')
    #                 text_owner,element_list_owner = get_th_text(element_root_owner, 'a')
    #                 for index, value in enumerate(text_owner):
    #                     result = contains_lang_chars(thai_ranges, value)
    #                     write_result(value, element_list_owner[index], result)
    #                 text_owner, element_list_owner = get_th_text(element_root_owner, 'span')
    #                 for index, value in enumerate(text_owner):
    #                     result = contains_lang_chars(thai_ranges, value)
    #                     write_result(value, element_list_owner[index], result)
    #             except Exception as e:
    #                 pass
    #         #type下，有property表格中有部分是带有code标签；需要单独检测
    #         if 'type' in result_url:
    #             try:
    #                 element_root_type=driver.find_element(By.XPATH,'//div[@class="app-markdown-ctx"]')
    #                 text_code,element_list_code=get_th_text(element_root_type, 'code')
    #                 for index, value in enumerate(text_code):
    #                     result = contains_lang_chars(thai_ranges, value)
    #                     write_result(value, element_list_code[index], result)
    #             except Exception as e:
    #                 pass
    #         print('======')

    #检测api，event，type这3个页面的内容
    # @test_print_name_th
    # def test_08_Firstlevel_Directory(self):
    #     for i in range(3):
    #         driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[{i + 1}]/div/div/a').click()
    #         time.sleep(0.5)
    #         WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,'//section[@class="app-docs-content"]')))
    #         element_root_middle = driver.find_element(By.XPATH, '//section[@class="app-docs-content"]').get_attribute('outerHTML')
    #         text_nav, element_list_nav = get_th_text(element_root_middle, 'span')
    #         for index, value in enumerate(text_nav):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list_nav[index], result)
    #         text_h1, element_list_h1 = get_th_text(element_root_middle, 'h1')
    #         for index, value in enumerate(text_h1):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list_h1[index], result)
    #         text_a, element_list_a = get_th_text(element_root_middle, 'a')
    #         for index, value in enumerate(text_a):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list_a[index], result)
    #         text_p, element_list_p = get_th_text(element_root_middle, 'p')
    #         for index, value in enumerate(text_p):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list_p[index], result)
    #
    #         element_root_aside = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/section/main/section/section/section/aside').get_attribute('outerHTML')
    #         text_div, element_list_div = get_th_text(element_root_aside, 'div')
    #         for index, value in enumerate(text_div):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list_div[index], result)
    #         text_aside_a, element_list_aside_a = get_th_text(element_root_aside, 'a')
    #         for index, value in enumerate(text_aside_a):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_list_aside_a[index], result)
    #
    # #检测modules分类下，每个种类的中间的内容
    # @test_print_name_th
    # def test_09_modules_middle(self):
    #     element_module_tab = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/aside/div/div[2]/div[1]/span')
    #     element_module_tab.click()
    #     for i in range(40):
    #         element = driver.find_element(By.XPATH,f'//*[@id="__nuxt"]/section/main/section/aside/div/div[4]/div/div/ul/li[{i + 1}]/div/div/a')
    #         element.click()
    #         time.sleep(0.5)
    #         # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__nuxt"]/section/main/section/section/section/section/section[1]/h1')))
    #         '''
    #         0722
    #         '''
    #         module_middle_root = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/section/main/section/section/section/section').get_attribute('outerHTML')
    #         module_aside_root = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/aside/div').get_attribute('outerHTML')
    #         print(element.get_attribute('textContent'))
    #
    #         text_a, element_a = get_th_text(module_middle_root, 'a')
    #         for index, value in enumerate(text_a):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_a[index], result)
    #
    #         text_h1, element_h1 = get_th_text(module_middle_root, 'h1')
    #         for index, value in enumerate(text_h1):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_h1[index], result)
    #
    #         text_span, element_span = get_th_text(module_middle_root, 'span')
    #         for index, value in enumerate(text_span):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_span[index], result)
    #
    #         text_th, element_th = get_th_text(module_middle_root, 'th')
    #         for index, value in enumerate(text_th):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_th[index], result)
    #
    #         text_td, element_td = get_th_text(module_middle_root, 'td')
    #         for index, value in enumerate(text_td):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_td[index], result)
    #
    #         WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/section/section[1]/section/div/div/div/div/div')))
    #         element_required_tips = driver.find_element(By.XPATH,'//div[@class="gfr-tooltip-content max-w-60 text-center"]')
    #         result=contains_lang_chars(thai_ranges, element_required_tips.get_attribute('textContent'))
    #         write_result(result, element_required_tips.get_attribute('outerHtml'), result)
    #
    #         text_aside_a, element_aside_a = get_th_text(module_aside_root, 'a')
    #         for index, value in enumerate(text_aside_a):
    #             result = contains_lang_chars(thai_ranges, value)
    #             write_result(value, element_aside_a[index], result)
    #
    #         element_aside_index = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/section/main/section/section/section/aside/div/div[1]')
    #         result=contains_lang_chars(thai_ranges, element_aside_index.get_attribute('textContent'))
    #         write_result(result, element_aside_index.get_attribute('outerHtml'), result)
    #         print('================')









