import numpy as np
import pandas as pd
data = pd.read_excel('C:\\Users\kxy\Desktop\\nantong\hailan.xlsx', encoding='gbk')
# columns = ['mysql自增ID', '商品ID', '商品名称', '店铺ID', '店铺名称', '卖家ID', '卖家名称', '类目ID',
#        '商品图片', '商品详情地址', '发货地区', '发货城市', '发货省份', '品牌', '商品参数', '商品促销价格',
#        '商品促销类型', '双十一价', '邮费', '库存', '商品点击数', '商品评论数', '商品收藏数', '30天购买人数,付款人数',
#        '30天购买件数，付款商品件数', '总销量', '30天销售额', '平台（0淘宝1天猫2淘宝企业）', '-', '-.1',
#        'partition_date']
# data.columns = columns
# print(data.loc[:, '商品名称'])
print(data.columns)
auction_name1 = data[data.商品名称.str.contains(r'.*?HLA.*?')][data.商品名称.str.contains(r'.*?海澜.*?')].loc[:, '商品名称'] #得到商品名称中包含HLA和海澜的
auction_name2 = data[data.商品名称.str.contains(r'.*?HLA.*?')].loc[:, '商品名称'] #得到商品名称中包含HLA
auction_name3 = list(set(auction_name2) ^ set(auction_name1)) #得到商品名称中包含HLA但不包括海澜的
condition = lambda i: r'HLA/?' not in i
auction_name4 = list(filter(condition, auction_name3)) #过滤掉包含HLA/?特殊情况的，剩下的就都不是海澜的产品
print(len(auction_name4))
auction_name5 = list(set(data.商品名称) ^ set(auction_name4)) #做差集得到所有的海澜之家的商品
data_filter = data[data.商品名称.isin(auction_name5)]
# print(data_filter)
new_data_filter = data_filter.drop_duplicates(subset=['商品ID', 'partition_date'], keep='last')
new_data_filter.to_csv('C:\\Users\kxy\Desktop\\nantong\hailan_filter.csv')

