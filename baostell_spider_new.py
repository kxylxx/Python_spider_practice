# -*- coding: utf-8 -*-
# 作者:孔翔玉

# 引入需要的第三方库
import os
import time
import re
import math
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# 记录程序开始时间
t1 = time.time()
# 设置数据保存路径
baostell_path = r'F:\baostell'
if not os.path.isdir(baostell_path):
    os.mkdir(baostell_path)
# 清空所有计划
df_plan_empty = pd.DataFrame()
df_plan_empty.to_csv(baostell_path + r'\plan.csv')
# 保存查询到的所有提单的详细信息
df_bill_empty = pd.DataFrame()
df_bill_empty.to_csv(baostell_path + r'\detail.csv')

# 启动浏览器，executable_path路径要根据自己chromedriver.exe的位置更改
driver = webdriver.Chrome(executable_path=r'E:\EXE\EXE\chromedriver_win32\chromedriver')
# 设置浏览器窗口位置及大小
driver.set_window_rect(x=0, y=0, width=667, height=748)
# 设定页面加载限制时间
driver.set_page_load_timeout(30)
# 设置锁定标签等待时长
wait = WebDriverWait(driver, 20)
# 打开登陆网址
driver.get('http://ets.baosteel.net.cn/ets_portal/')
# 模拟js操作向下滑动窗口到最底部
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# 进行登陆
driver.switch_to.frame("login")
time.sleep(0.5)
driver.find_element_by_id("p_username").clear()
driver.find_element_by_id("p_username").send_keys('U07210')
driver.find_element_by_name("userLoginPsd").clear()
driver.find_element_by_name("userLoginPsd").send_keys('060811')
# 手动输入验证码
input_code = input("请输入验证码:")
driver.find_element_by_name("ccode").clear()
driver.find_element_by_name("ccode").send_keys(input_code)
driver.find_element_by_id("button2").click()
driver.switch_to.default_content()

# 进入业务页面
element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "业务承接")))
element.click()
element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "业务承接计划")))
element.click()
driver.switch_to.frame('content')
element = wait.until(EC.presence_of_element_located((By.ID, 'beginTransPlanDateStr')))
element.click()
iframe = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/iframe')))
driver.switch_to.frame(iframe)
# 设置起始计划日期
begin_data = input('请依次输入起始计划日期(样例：2018-1-2,非2018-01-02)：')
begin_data_list = begin_data.split('-')
time.sleep(0.5)
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

# 设置结束计划日期
driver.switch_to.parent_frame()
driver.find_element_by_name('endTransPlanDateStr').click()
iframe = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/iframe')))
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

# 开始查询
driver.switch_to.parent_frame()
driver.find_element_by_id('btn0').click()
# 让程序暂停1秒，以便于页面加载
time.sleep(1)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
content_plan_list = driver.page_source.encode('utf-8')  # 获取网页内容
# 解析网页
soup = BeautifulSoup(content_plan_list, "lxml")
# 获取id="next_page"的标签
text = soup.find(id="next_page")
# 给记录条数设个初始值，使其成为全局变量
record_num = 0
# 保存plan列表中的数据
df_plan_lists = pd.DataFrame({})
# 保存表单的详细信息
df_bill_all = pd.DataFrame({})

if text:
    # 生成一个局部变量
    df_plan_list = pd.DataFrame({})
    # 利用正则表达式得到查询到多少条记录
    record_num = re.search(r'.*?共(\d*?)条记录', str(text), re.S).group(1)
    print('本次查询共有{}条记录'.format(record_num))
    # 根据记录个数利用for循环进行翻页
    for m in range(int(math.ceil((int(record_num)/20)))):
        df_plan_list.drop(df_plan_list.index, inplace=True)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        # 解析计划列表内容，每条内容以字典类型存储于plan_dict变量中，key_list是获得字典的键的，也就是表头
        tables = soup.select_one('#chaxun > div.chaxun_block > table')
        items = tables.find_all('tr')
        key_list = []
        plan_dict = {}
        # 解析表头
        tds = items[0].find_all('th')
        for key in tds[1:]:
            key_list.append(key.get_text(strip=True))
        # print(key_list)
        # 解析整个列表
        for item in items[1:]:
            tds = item.find_all('td')
            j = 0
            for td in tds[1:]:
                plan_dict[key_list[j]] = td.get_text(strip=True)
                j = j+1
            # print(plan_dict)
            df_plan_list = df_plan_list.append(plan_dict.copy(), ignore_index=True)
        # 将该页面计划列表内容加入到记录总计划列表的变量中，df_plan_lists用来记录查询到的所有计划列表内容
        df_plan_lists = df_plan_lists.append(df_plan_list.copy())
        # print(df_plan_list)

        # 下面开始进入及解析记录细节的页面
        bill_key_list = []
        bill_dict = {}
        # 用来记录每个提单的详细数据
        df_bill = pd.DataFrame({})
        checkboxes = wait.until(EC.presence_of_all_elements_located((By.NAME, 'checkbox')))
        # 利用for循环依次解析计划列表中的所有提单
        for i_check in range(len(checkboxes)):
            # 清空df_bill
            df_bill.drop(df_bill.index, inplace=True)
            # print(i_check)
            # print('len', len(checkboxes))
            # 计划列表是js动态加载的只有当其显示出来时才会加载出来，所以当解析后面的提单时需要下滑页面
            if i_check > 8:
                driver.execute_script('window.scrollTo(0, document.body.clientHeight)')
            # 一次只能提交一个提单，所以要把上一个选择去掉，再选下一个选择
            if i_check > 0:
                checkbox = checkboxes[i_check-1]
                checkbox.click()
                time.sleep(0.5)
            checkbox = checkboxes[i_check]
            checkbox.click()
            # 点击提单打印
            driver.find_element_by_id('btn9').click()
            time.sleep(1)
            # 转到提单详情页面中，然后解析网页内容
            driver.switch_to.window(driver.window_handles[-1])
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "toolbar")))
            num_of_items = df_plan_list.loc[i_check, '计划件数']
            print('计划件数：', num_of_items)
            # 下面几个if判断可以使用一个for循环解决后面再优化
            if int(num_of_items) > 0:
                content = driver.page_source.encode('utf-8')  # 获取网页内容
                soup = BeautifulSoup(content, "lxml")
                tables = soup.find(id='divArea0_40')
                items = tables.find_all('tr')  # 找到table标签下的除第一行外的所有tr标签，返回的是列表
                tds = items[0].find_all('td')
                for key in tds:
                    bill_key_list.append(key.get_text(strip=True))

                for item in items[1:]:
                    tds = item.find_all('td')
                    num_td = 0
                    for td in tds:
                        bill_dict[bill_key_list[num_td]] = td.get_text(strip=True)
                        num_td = num_td + 1
                    df_bill = df_bill.append(bill_dict.copy(), ignore_index=True)

            if int(num_of_items) > 38:
                driver.find_element_by_css_selector('#toolbarTbl > tbody > tr > td:nth-child(2) > a').click()
                time.sleep(1)
                content = driver.page_source.encode('utf-8')  # 获取网页内容
                soup = BeautifulSoup(content, "lxml")
                tables = soup.find(id='divArea1_1')
                items = tables.find_all('tr')  # 找到table标签下的除第一行外的所有tr标签，返回的是列表
                tds = items[0].find_all('td')
                for key in tds:
                    bill_key_list.append(key.get_text(strip=True))

                for item in items[1:]:
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
                    time.sleep(1)
                    content = driver.page_source.encode('utf-8')  # 获取网页内容
                    soup = BeautifulSoup(content, "lxml")
                    tables = soup.find(id='divArea{}_1'.format((k+2)))
                    items = tables.find_all('tr')  # 找到table标签下的除第一行外的所有tr标签，返回的是列表
                    tds = items[0].find_all('td')
                    for key in tds:
                        bill_key_list.append(key.get_text(strip=True))

                    for item in items[1:]:
                        tds = item.find_all('td')
                        num_td2 = 0
                        for td in tds:
                            bill_dict[bill_key_list[num_td2]] = td.get_text(strip=True)
                            num_td2 = num_td2 + 1
                        df_bill = df_bill.append(bill_dict.copy(), ignore_index=True)
            # 去掉总计那行
            df_bill = df_bill.iloc[:-1, :]
            # 在提单详情数据中加入计划号
            df_bill['计划号'] = df_plan_list.loc[i_check, '计划号']
            # print("df_bill:", df_bill)
            # 将单个提单数据汇总到所有提单数据集合中
            df_bill_all = df_bill_all.append(df_bill.copy())
            # print("df_bill_all:", df_bill_all)
            # 将提单详情页关闭
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            # time.sleep(1)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#contentIframe')))
            driver.switch_to.frame('content')
            checkboxes = wait.until(EC.presence_of_all_elements_located((By.NAME, 'checkbox')))
        try:
            element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.LINK_TEXT, '下一页')))
            element.click()
            time.sleep(1)
            content_plan_list = driver.page_source.encode('utf-8')  # 获取网页内容
            soup = BeautifulSoup(content_plan_list, "lxml")
        except TimeoutException:
            print("已获取到所有计划")
df_bill_all[['材料号']] = df_bill_all[['材料号']].astype(str)

# 保存查询到的所有计划
df_plan_lists.to_csv(baostell_path + r'\plan.csv')
# 保存查询到的所有提单的详细信息
df_bill_all.to_csv(baostell_path + r'\detail.csv')
# print(df_bill_all)
t2 = time.time()
print('程序运行时间为{}秒'.format((t2-t1)))
b = input('点击任意键，后点enter结束')
driver.quit()