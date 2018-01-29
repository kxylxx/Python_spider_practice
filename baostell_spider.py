# -*- coding: utf-8 -*-
# 作者:孔翔玉


import os
import time
import re

import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

t1 = time.time()

driver = webdriver.Chrome(executable_path=r'E:\EXE\EXE\chromedriver_win32\chromedriver')
driver.set_window_rect(x=0, y=0, width=1050, height=748)
# 设定页面加载限制时间
driver.set_page_load_timeout(30)
driver.get('http://ets.baosteel.net.cn/ets_portal/')

driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
driver.switch_to.frame("login")
time.sleep(0.5)
driver.find_element_by_id("p_username").clear()
driver.find_element_by_id("p_username").send_keys('U07210')
driver.find_element_by_name("userLoginPsd").clear()
driver.find_element_by_name("userLoginPsd").send_keys('060811')
mycode = input("请输入验证码:")
driver.find_element_by_name("ccode").clear()
driver.find_element_by_name("ccode").send_keys(mycode)
driver.find_element_by_id("button2").click()
driver.switch_to.default_content()
# 设置等待时长
wait = WebDriverWait(driver, 15)

element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "业务承接")))
element.click()
element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "业务承接计划")))
element.click()


driver.switch_to.frame('content')
element = wait.until(EC.presence_of_element_located((By.ID, 'beginTransPlanDateStr')))
element.click()
iframe = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/iframe')))
driver.switch_to.frame(iframe)

begin_data = input('请依次输入起始计划日期(样例：2018-1-2,非2018-01-02)：')
begin_data_list = begin_data.split('-')
b_year = begin_data_list[0]
b_month = begin_data_list[1]
b_day = begin_data_list[2]
begin_year = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dpTitle"]/div[4]/input')))
begin_year.clear()
begin_year.send_keys(b_year)
begin_month = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dpTitle"]/div[3]/input')))
# begin_month = driver.find_element_by_xpath('//*[@id="dpTitle"]/div[3]/input')
begin_month.clear()
begin_month.send_keys(b_month)
begin_month.click()
begin_days = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/table')))
begin_days.click()
driver.find_element_by_xpath(
    '/html/body/div/div[3]/table/tbody/tr/td[@onclick="day_Click({year},{month},{day});"]'.format(year=b_year, month=b_month, day=b_day)).click()

driver.switch_to.parent_frame()
driver.find_element_by_name('endTransPlanDateStr').click()
iframe = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/iframe')))
# iframe = driver.find_element_by_xpath('/html/body/div[7]/iframe')
driver.switch_to.frame(iframe)
end_data = input('请依次输入结束计划日期(样例：2018-1-2,非2018-01-02)：')
end_data_list = end_data.split('-')
e_year = end_data_list[0]
e_month = end_data_list[1]
e_day = end_data_list[2]

end_year = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dpTitle"]/div[4]/input')))
end_year.clear()
end_year.send_keys(e_year)
end_month = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="dpTitle"]/div[3]/input')))
end_month.clear()
end_month.send_keys(e_month)
end_month.click()
end_days = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/table')))
end_days.click()
driver.find_element_by_xpath(
    '/html/body/div/div[3]/table/tbody/tr/td[@onclick="day_Click({year},{month},{day});"]'.format(year=e_year, month=e_month, day=e_day)).click()


driver.switch_to.parent_frame()
driver.find_element_by_id('btn0').click()
time.sleep(2)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
content_plan_list = driver.page_source.encode('utf-8')  # 获取网页内容
soup = BeautifulSoup(content_plan_list, "lxml")
text = soup.find(id="next_page")
# 给记录条数设个初始值，使其成为全局变量
record_num = 0
# 保存plan列表中的数据
df_plan_lists = pd.DataFrame({})
# 保存表单的详细信息
df_bill_all = pd.DataFrame({})

if text:
    df_plan_list = pd.DataFrame({})
    record_num = re.search(r'.*?共(\d*?)条记录', str(text), re.S).group(1)
    print('本次查询共有{}条记录'.format(record_num))
    for m in range(int(math.ceil((int(record_num)/20)))):
        df_plan_list.drop(df_plan_list.index, inplace=True)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)

        tables = soup.select_one('#chaxun > div.chaxun_block > table')
        items = tables.find_all('tr')

        key_list = []
        plan_dict = {}
        tds = items[0].find_all('th')
        for key in tds[1:]:
            key_list.append(key.get_text(strip=True))
        # print(key_list)
        for item in items[1:]:
            tds = item.find_all('td')
            j = 0
            for td in tds[1:]:
                plan_dict[key_list[j]] = td.get_text(strip=True)
                j = j+1
            # print(plan_dict)
            df_plan_list = df_plan_list.append(plan_dict.copy(), ignore_index=True)
        df_plan_lists = df_plan_lists.append(df_plan_list.copy())
        # print(df_plan_list)

        bill_key_list = []
        bill_dict = {}
        df_bill = pd.DataFrame({})
        checkboxes = wait.until(EC.presence_of_all_elements_located((By.NAME, 'checkbox')))

        for i_check in range(len(checkboxes)):
            df_bill.drop(df_bill.index, inplace=True)
            print(i_check)
            # checkboxes = driver.find_elements_by_name('checkbox')
            print('len', len(checkboxes))
            if i_check > 8:
                driver.execute_script('window.scrollTo(0, document.body.clientHeight)')
            checkbox = checkboxes[i_check]
            checkbox.click()

            driver.find_element_by_id('btn9').click()
            time.sleep(1)
            # 要转到新的连接上去，然后解析网页内容
            driver.switch_to.window(driver.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toolbar")))
            num_of_items = df_plan_list.loc[i_check, '计划件数']
            print('计划件数：', num_of_items)
            if int(num_of_items) > 0:
                content = driver.page_source.encode('utf-8')  # 获取网页内容
                soup = BeautifulSoup(content, "lxml")
                tables = soup.find(id='divArea0_40')
                items = tables.find_all('tr')  # 找到table标签下的除第一行外的所有tr标签，返回的是列表
                tds = items[0].find_all('td')
                for key in tds:
                    bill_key_list.append(key.get_text(strip=True))

                for item in items[1:-1]:
                    tds = item.find_all('td')
                    num_td = 0
                    for td in tds:
                        bill_dict[bill_key_list[num_td]] = td.get_text(strip=True)
                        num_td = num_td + 1
                    df_bill = df_bill.append(bill_dict.copy(), ignore_index=True)

            if int(num_of_items) > 38:
                driver.find_element_by_css_selector('#toolbarTbl > tbody > tr > td:nth-child(2) > a').click()
                time.sleep(2)
                content = driver.page_source.encode('utf-8')  # 获取网页内容
                soup = BeautifulSoup(content, "lxml")
                tables = soup.find(id='divArea1_1')
                items = tables.find_all('tr')  # 找到table标签下的除第一行外的所有tr标签，返回的是列表
                tds = items[0].find_all('td')
                for key in tds:
                    bill_key_list.append(key.get_text(strip=True))

                for item in items[1:-1]:
                    tds = item.find_all('td')
                    num_td1 = 0
                    for td in tds:
                        bill_dict[bill_key_list[num_td1]] = td.get_text(strip=True)
                        num_td1 = num_td1 + 1

                    df_bill = df_bill.append(bill_dict.copy(), ignore_index=True)
                # time.sleep(0.5)
            if int(num_of_items) > 83:
                for k in range(int(math.ceil((int(num_of_items)-83)/45))):
                    driver.find_element_by_xpath('//*[@id="toolbarTbl"]/tbody/tr/td[4]/a').click()
                    time.sleep(2)
                    content = driver.page_source.encode('utf-8')  # 获取网页内容
                    soup = BeautifulSoup(content, "lxml")
                    tables = soup.find(id='divArea{}_1'.format((k+2)))
                    items = tables.find_all('tr')  # 找到table标签下的除第一行外的所有tr标签，返回的是列表
                    tds = items[0].find_all('td')
                    for key in tds:
                        bill_key_list.append(key.get_text(strip=True))

                    for item in items[1:-1]:
                        tds = item.find_all('td')
                        num_td2 = 0
                        for td in tds:
                            bill_dict[bill_key_list[num_td2]] = td.get_text(strip=True)
                            num_td2 = num_td2 + 1
                        df_bill = df_bill.append(bill_dict.copy(), ignore_index=True)
            df_bill['计划号'] = df_plan_list.loc[i_check, '计划号']
            # print("df_bill:", df_bill)
            # pd.concat([df_bill_all, df_bill])
            df_bill_all = df_bill_all.append(df_bill.copy())
            # print("df_bill_all:", df_bill_all)
            driver.close()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#contentIframe')))
            driver.switch_to.frame('content')
            element = wait.until(EC.presence_of_element_located((By.ID, 'btn0')))
            # driver.find_element_by_id('btn0').click()
            element.click()
            time.sleep(2)

            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            if m > 0:
                print('m:', m)
                element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, str(m+1))))
                element.click()
                # element.send_keys((m+1))
                # time.sleep(5)
                # element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="next_page"]/a[6]')))
                # element.click()
                time.sleep(2)
                content_plan_list = driver.page_source.encode('utf-8')  # 获取网页内容
                soup = BeautifulSoup(content_plan_list, "lxml")
            checkboxes = wait.until(EC.presence_of_all_elements_located((By.NAME, 'checkbox')))
        try:
            element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, '下一页')))
            element.click()
            time.sleep(2)
            content_plan_list = driver.page_source.encode('utf-8')  # 获取网页内容
            soup = BeautifulSoup(content_plan_list, "lxml")
        except NoSuchElementException:
            print("已获取到所有计划")
df_bill_all[['材料号']] = df_bill_all[['材料号']].astype(str)

baostell_path = r'F:\baostell'
if not os.path.isdir(baostell_path):
    os.mkdir(baostell_path)

df_plan_lists.to_csv(baostell_path + r'\plan.csv')
df_bill_all.to_csv(baostell_path + r'\detail.csv')
# print(df_bill_all)
t2 = time.time()
print('程序运行时间为{}秒'.format((t2-t1)))
b = input('点击任意键，后点enter结束')
driver.quit()