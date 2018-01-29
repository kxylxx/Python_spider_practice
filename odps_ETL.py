# -*- coding: utf-8 -*-

'''连接阿里云读取相关数据并且操作对应的表'''
import pandas as pd
hla_data = pd.read_excel(r'C:\Users\Think\Desktop\hla.xlsx')
# print(hla_data)
#统计c店和b店的占比关系
Business_shop = 0
Customer_shop = 0
for shop_name in hla_data['shop_name']:
    if '旗舰店' in str(shop_name):
        Business_shop += 1
    else:
        Customer_shop += 1
print(Business_shop/len(hla_data['shop_name']),Customer_shop/len(hla_data['shop_name']))

#统计每个月所有店铺的总的销售额销售额
Sept_sale_count = 0
July_sale_count = 0
June_sale_count = 0
Sept_series = hla_data.ix[hla_data.partition_data == '20170930','amount_30days']
print(Sept_series)
print(Sept_sale_count,July_sale_count,June_sale_count)

# 统计店铺和地区销量的排序
sort_shop_name = hla_data['shop_name'].value_counts()
sort_region = hla_data['region'].value_counts()
sort_sale_total = hla_data['']
with open('f2.txt', 'w',encoding='utf-8') as f2:
    f2.write(str(sort_shop_name))
    f2.write('/n')
    f2.write(str(sort_region))