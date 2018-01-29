# -*- coding: utf-8 -*-

import pandas as pd
df = pd.read_csv('F:\\baostell\\2.csv', encoding='gbk', dtype={'材料号': str})
print(df)
