import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
# phantomjs_path = r'E:\EXE\EXE\phantomjs-2.1.1-windows\bin\phantomjs'
df = pd.DataFrame({})
driver = webdriver.Chrome(executable_path=r'E:\EXE\EXE\chromedriver_win32\chromedriver_1')
# 设定页面加载限制时间
driver.set_page_load_timeout(30)
driver.get('http://www.kuaidi100.com/')
print('cookies:', driver.get_cookies())
driver.find_element_by_name("postid").clear()  # 清空输入框内容
driver.find_element_by_name("postid").send_keys('3346535929281')  # 输入订单号
driver.find_element_by_id("query").click()  # 点击搜索按钮
time.sleep(3)
content = driver.page_source.encode('utf-8')  # 获取网页内容
soup = BeautifulSoup(content, "lxml")  # 解析网页

items = soup.table.find_all('tr')  # 找到table标签下的所有tr标签，返回的是列表
for item in items:
    td = item.find_all('td')  # 找到所有td标签
    # print(td[0])
    time = [i.string for i in td[0].find_all('span')]  # 获取各送货节点时间
    location = td[2].string  # 获取送货节点位置信息
    if not location:
        location = [i for i in td[2].strings][0] + [i for i in td[2].strings][-1]
    # print(location)
    data = {
        "time": time,
        "location": location
    }
    df = df.append(data, ignore_index=True)
print(df)
# driver.quit()
driver.close()
df.to_csv('F:\kuaidi100.csv')
