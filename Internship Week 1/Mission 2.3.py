import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


user = pd.read_csv('users.csv',encoding='gbk')
user.head()

#处理缺失、重复值
user = user.drop_duplicates()
user['school'] = user['school'].fillna('unknown')
dif = user['recently_logged'] == '--'
user.loc[dif,'recently_logged'] = user.loc[dif,'register_time']



#截止时间为2020/6/18,即2020/6/19起正式结束，则计算2020/6/19与最后登录时间的时间差
Due = '2020/6/19'
user['diff'] = (pd.to_datetime(Due) - pd.to_datetime(user['recently_logged'])).dt.days
diff = user['diff']
loss_ = user[user['diff'] > 90]


print('流失率为：{0}'.format(len(loss_)/len(diff)))


sns.kdeplot(diff)
