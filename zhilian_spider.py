import os
import random
from urllib.parse import urlencode

import pandas as pd
import requests
from multiprocessing import Pool

import time
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
import json
from pyquery import PyQuery as pq


def get_pages(url, user_agent_list):
    headers = {'User-Agent': random.choice(user_agent_list)}
    try:
        response = requests.get(url, headers=headers)
        # print(response.text)
        if response.status_code == 200:
            doc = pq(response.text)
            # print(doc)
            urls_tag = doc('#newlist_list_content_table table.newlist').items()
            for url_tag in urls_tag:
                # print(url_tag)
                url = url_tag('div a:nth-child(1)').attr('href')
                # yield url
                if url:
                    time.sleep(1)
                    yield url
            print(doc('li.pagesDown-pos a').attr('href'))
            if doc('li.pagesDown-pos a').attr('href'):
                for url in get_pages(doc('li.pagesDown-pos a').attr('href'), user_agent_list):
                    time.sleep(3)
                    yield url
        else:
            yield None
    except RequestException:
        yield None


def get_one_page(url, user_agent_list):
    headers = {'User-Agent': random.choice(user_agent_list)}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(url, html):
    # item = {'职位名称':[],'工作地点':[],'公司性质':[],'公司规模':[],'学历':[],'职位月薪':[],'岗位职责':[]}
    # print(html)
    soup = BeautifulSoup(html, "lxml")  # 设置解析器为“lxml”
    if soup.select('div.fixed-inner-box h1'):
        occ_name = soup.select('div.fixed-inner-box h1')[0]
        com_name = soup.select('div.fixed-inner-box h2')[0]
        com_url = soup.select('div.inner-left.fl h2 a')[0]
        welfare = soup.select('div.welfare-tab-box')[0]
        wages = soup.select('div.terminalpage-left strong')[0]
        date = soup.select('div.terminalpage-left strong')[2]
        exper = soup.select('div.terminalpage-left strong')[4]
        num = soup.select('div.terminalpage-left strong')[6]
        area = soup.select('div.terminalpage-left strong')[1]
        nature = soup.select('div.terminalpage-left strong')[3]
        Edu = soup.select('div.terminalpage-left strong')[5]
        cate = soup.select('div.terminalpage-left strong')[7]
        com_scale = soup.select('ul.terminal-ul.clearfix li strong')[8]
        com_nature = soup.select('ul.terminal-ul.clearfix li strong')[9]
        com_cate = soup.select('ul.terminal-ul.clearfix li strong')[10]
        com_address = soup.select('ul.terminal-ul.clearfix li strong')[11]
        job_describe = soup.select('div.tab-inner-cont')[0].find_all('p')
        describe = []
        for i in job_describe:
            if i.string:
                describe.append(i.string.strip())
        data = {
            "网址": url,
            "工作名称": occ_name.text.strip(),
            "公司名称": com_name.text,
            "公司网址": com_url.get('href'),
            "福利": welfare.text.strip(),
            "月工资": wages.text.strip(),
            "发布日期": date.text.strip(),
            "经验": exper.text.strip(),
            "人数": num.text.strip(),
            "工作地点": area.text.strip(),
            "工作性质": nature.text.strip(),
            "最低学历": Edu.text.strip(),
            "职位类别": cate.text.strip(),
            "职位描述": ''.join(describe),
            "公司规模": com_scale.text.strip(),
            "公司性质": com_nature.text.strip(),
            "公司行业": com_cate.text.strip(),
            "公司地址": com_address.text.strip()
        }
        return data
    else:
        print('未采集到网址：', url)
        return None


def main(city, keyword):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"
    ]
    page = 1
    data = {
        'jl': city,
        'kw': keyword,
        'sm': 0,
        'p': page
    }
    par = urlencode(data)
    base = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'
    initial_url = base + par
    print(initial_url)
    # urls = get_pages(initial_url, headers)
    # print(urls)
    df = pd.DataFrame({})
    for url in get_pages(initial_url, user_agent_list):
        print('url:', url)
        if url:
            html = get_one_page(url, user_agent_list)
            if html:
                item = parse_one_page(url, html)
                if item:
                    df = df.append(item, ignore_index=True)
            else:
                print('未采集到网址：', url)

            # print(df)
    # for item in parse_one_page(html):
    #     print(item)
    #     write_to_file(item)
    df.to_csv(zhilianPath + r'\{}_{}.csv'.format(city, keyword))


if __name__ == '__main__':
    zhilianPath = r'F:\智联'
    if not os.path.isdir(zhilianPath):
        os.mkdir(zhilianPath)
    main(city='南京', keyword='数据') #keyword代表要搜索职位的关键字
    # pool = Pool(processes=1)
    # pool.map(main, [i*10 for i in range(10)])