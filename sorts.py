# -*- coding: utf-8 -*-
# def largestRectangleArea(height):
#     height.append(0)
#     size = len(height)
#     no_decrease_stack = [0]
#     max_size = height[0]
#     i = 0
#     while i < size:
#         cur_num = height[i]
#         if (not no_decrease_stack or
#                     cur_num > height[no_decrease_stack[-1]]):
#             no_decrease_stack.append(i)
#             i += 1
#             print(i, no_decrease_stack, 'a')
#         else:
#             index = no_decrease_stack.pop()
#             if no_decrease_stack:
#                 width = i - no_decrease_stack[-1] - 1
#             else:
#                 width = i
#             print(i, no_decrease_stack, width, height[index])
#             max_size = max(max_size, width * height[index])
#     return max_size
# height = [2, 1, 5, 6]
# result = largestRectangleArea(height=height)
# print(result)
import json

import requests
from urllib import request
url = "http://so.eastmoney.com/Web/GetSearchList?type=20&pageindex=1&pagesize=10&keyword=%E5%91%A8%E6%B5%B7%E6%B1%9F"
payload = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"}
response = requests.get(url, headers=payload)
print(response.status_code)
print(response.text)
# print(json.loads(response.text))
# a = r'{"IsSuccess":true,"Code":0,"Message":"成功","TotalPage":11,"TotalCount":107,"Keyword":"周海江","Data":[{"Art_Title":"红豆股份获大股东增持5%股份","Art_Url":"http://finance.eastmoney.com/news/1354,20170918777869873.html","Art_CreateTime":"2017-09-18 07:21:36","Art_Content":" 　　红豆股份今日发布公告称，公司于9月15日收到大股东红豆集团有限公司及其一致行动人\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e、周耀庭、顾建清、王竹倩、蒋雄伟、郭建军、朱文玉的《简式权益变动报告书》，红豆集团及其一致行动人通过上海证券交易所交易系统已累计增持红豆股份9047万股，占公司总股份的5.00%。截至..."},{"Art_Title":"红豆股份控股股东方面增持达5%","Art_Url":"http://finance.eastmoney.com/news/1349,20170915777669483.html","Art_CreateTime":"2017-09-15 22:10:59","Art_Content":"　　 红豆股份15日晚间公告，控股股东红豆集团及其一致行动人\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e、周耀庭、顾建清、王竹倩、蒋雄伟、郭建军、朱文玉已累计增持红豆股份90,473,406股，占公司总股份的5%。截至2017年9月15日，红豆集团及其一致行动人合计持有红豆股份普通股股份1,092,622,642股，占公司总股份的60.38%。..."},{"Art_Title":"快人一步！坚守实业的红豆物联网布局","Art_Url":"http://finance.eastmoney.com/news/1586,20170913776561477.html","Art_CreateTime":"2017-09-13 11:27:38","Art_Content":"目光。该基金由感知集团、红豆集团、远东控股、海融资本等几家企业联合发起。全国工商联副主席、红豆集团董事局主席兼CEO\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e在会议上分享了作为长期坚守实体经济的代表，红豆在物联网大潮中快人一步的布局。\r\n 　　放眼全球，物联网产业正在迎来前所未有的应用“爆发期”，这已经成为各界的..."},{"Art_Title":"60华诞不忘回馈社会 红豆捐赠1000万元","Art_Url":"http://finance.eastmoney.com/news/1586,20170907774749385.html","Art_CreateTime":"2017-09-07 15:05:50","Art_Content":"今年继“无锡耀庭慈善基金会”关爱百岁老人活动、红豆集团董事局主席兼CEO\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e个人出资2000万元设立“无锡红豆关爱老党员基金”、“中国光彩事业凉山行”捐赠200万元支持当地公益事业后的又一次公益壮举。　　感恩情怀引领红豆积极履责　　于企业而言，感恩是一种情怀，也是一种文化，只有..."},{"Art_Title":"大股东一再增持 红豆股份为爱而行","Art_Url":"http://finance.eastmoney.com/news/1586,20170906774378330.html","Art_CreateTime":"2017-09-06 17:41:29","Art_Content":"实业的有力见证。红豆集团及一致行动人对公司未来发展及市场投资前景充满了信心。\r\n 　　红豆股份一直注重社会责任，积极践行“八方共赢”的理念。红豆集团董事局主席\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e说，所谓八方共赢，就是努力实现与股东、员工、顾客、供方、合作伙伴、政府、环境、社会(社区)等八个利益相关方的共赢。增持..."},{"Art_Title":"红豆股份 控股股东等拟继续增持","Art_Url":"http://finance.eastmoney.com/news/1354,20170904773272642.html","Art_CreateTime":"2017-09-04 07:43:41","Art_Content":" 　　红豆股份9月3日晚间发布公告称，公司控股股东红豆集团及其一致行动人\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e、周耀庭、顾建清、王竹倩、蒋雄伟、郭建军6月1日至今累计增持公司股份5369.02万股，增持比例2.967%，完成于今年6月披露的增持计划。本次增持后，前述股东合计持股比例达58.73%，同时红豆集团及其一致行动人计划在12个月内继续增持公司股份，增持比例为1%-5%。..."},{"Art_Title":"红豆股份向“智慧化”转型 上半年净利增7倍","Art_Url":"http://finance.eastmoney.com/news/1354,20170904773245095.html","Art_CreateTime":"2017-09-04 01:44:23","Art_Content":"使生产效率比普通设备提高三倍以上。\r\n 　　除了自动化节约人工成本外，数年之前，红豆股份母公司，红豆集团董事局主席兼CEO\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e还提出了“创新领先”理念，从2010年开始，红豆股份启动男装经营模式转型，着力推进在零售管理、供应链组织上逐步强化升级。新模式的确立，让公司品牌服装..."},{"Art_Title":"\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e：“一带一路”项目必须扎根当地人民","Art_Url":"http://finance.eastmoney.com/news/1586,20170623749796168.html","Art_CreateTime":"2017-06-23 17:13:46","Art_Content":"。\r\n 　　6月22日，全国工商联为深入学习贯彻习近平总书记系列重要讲话精神，引导民营企业坚定信心、守法诚信，积极投身实体经济和供给侧结构性改革，主动参与“一带一路”建设，所以在中央社会主义学院举办了全联直属会员培训班，特邀请全国工商联副主席、红豆集团董事局主席\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e为百名会员..."},{"Art_Title":"沪市上市公司公告(6月9日)","Art_Url":"http://stock.eastmoney.com/news/1391,20170608745179134.html","Art_CreateTime":"2017-06-08 22:27:51","Art_Content":"(600400)发布公告称，6月1日至6月8日期间，公司控股股东红豆集团及其一致行动人周耀庭、\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e、顾建清、王竹倩、蒋雄伟通过上海证券交易所交易系统增持红豆股份12,399,517股，占公司总股份的0.685%。　　棕榈股份：栖霞建设拟减持不超1377万股　　棕榈股份(002431..."},{"Art_Title":"红豆股份获控股股东及其一致行动人增持1239.95万股","Art_Url":"http://finance.eastmoney.com/news/1354,20170608745176567.html","Art_CreateTime":"2017-06-08 22:03:29","Art_Content":" 　　红豆股份8日晚间公告，6月1日至6月8日期间，公司控股股东红豆集团及其一致行动人周耀庭、\u003cem\u003e周\u003c/em\u003e\u003cem\u003e海\u003c/em\u003e\u003cem\u003e江\u003c/em\u003e、顾建清、王竹倩、蒋雄伟通过上海证券交易所交易系统增持红豆股份12,399,517股，占公司总股份的0.685%。..."}],"RelatedWord":""}'
# print(json.loads(a))