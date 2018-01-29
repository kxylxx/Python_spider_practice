import time

from selenium import webdriver
from selenium.webdriver import ActionChains

phantomjs_path = r'E:\EXE\EXE\phantomjs-2.1.1-windows\bin\phantomjs'

driver = webdriver.Chrome(executable_path=r'E:\EXE\EXE\chromedriver_win32\chromedriver')
# 设定页面加载限制时间
driver.set_page_load_timeout(15)
driver.get('http://signin.aliyun.com/1174770817896247/login.htm')
driver.find_element_by_name("user_principal_name").clear()
driver.find_element_by_name("user_principal_name").send_keys('nju@1174770817896247')
driver.find_element_by_id("J_FormNext").click()
time.sleep(3)
driver.find_element_by_id("password_ims").send_keys('nju123456')
driver.find_element_by_id("u22").click()
driver.get('https://ide-cn-shanghai.data.aliyun.com/?projectId=')
time.sleep(5)
driver.find_element_by_link_text('我知道了').click()
time.sleep(3)
driver.find_element_by_link_text('我知道了').click()
time.sleep(3)
driver.find_element_by_link_text('我知道了').click()
time.sleep(3)
driver.find_element_by_link_text('我知道了').click()
time.sleep(3)
driver.find_element_by_link_text('完成').click()
time.sleep(5)
driver.find_element_by_link_text('脚本开发').click()
time.sleep(2)
try:
    for i in range(2):
        double_click1 = driver.find_element_by_css_selector('.tree-label.locker.label.label-success')
        ActionChains(driver).double_click(double_click1).perform()
        ActionChains(driver).double_click(double_click1).perform()
        time.sleep(3)
except Exception as e:
    print(e)

# js = "document.getElementsByClassName(\"cm-variable\").innerHTML='select * from tao_auction where id between 0 and 10000'"
js = 'var change = document.getElementById("J_trix_2").getElementsByTagName("span")[4].innerHTML="select * from tao_auction where id between 0 and 10000";'
#
# # js1 = 'var change = document.getElementById("J_trix_2").getElementsByTagName("span")[2].innerHTML="";'
# # js2 = 'var change = document.getElementById("J_trix_2").getElementsByTagName("span")[3].innerHTML="";'
#
# # js = '''var para=document.createElement("span");var node=document.createTextNode("select");para.appendChild(node);var element=document.getElementById("J_trix_2").getElementsByTagName("span")[1];element.appendChild(para);'''
driver.execute_script(js)

# driver.execute_script(js1)
# driver.execute_script(js2)

# print(a.text)
# print(driver.find_element_by_xpath(
#     '//*[@id="J_trix_2"]/div/div/div[2]/div/div[6]/div[1]/div/div/div/div[5]/div/pre/span/span[1]').text)
# change_content = driver.find_elements_by_xpath(
#     '//*[@id="J_trix_2"]/div/div/div[2]/div/div[6]/div[1]/div/div/div/div[5]/div/pre/span/span')
# for i in change_content:
#     print(i.submit())
# driver.find_element_by_xpath(
#     '//*[@id="J_trix_2"]/div/div/div[2]/div/div[6]/div[1]/div/div/div/div[5]/div/pre//span[@class="cm-variable"]').send_keys(
#     'select * from business_data.tao_auction where id between 0 and 10000')
# driver.find_element_by_xpath('//*[@id="22377801"]/div/div[1]/div/nav/div/ul/li[1]/a/span').click()
# time.sleep(3)
# driver.find_element_by_xpath('//*[@id="J_trix_3"]/div/div[2]/div/div[3]/button[1]').click()
# time.sleep(60)
# driver.find_element_by_xpath('//*[@id="da1876b7-8a9e-49e3-8b16-3771b8c7352d"]/div[2]/ul[1]/li[2]/a').click()

# driver.find_element_by_xpath('//*[@id="J_trix_2"]//div[@class="CodeMirror-code"]')
