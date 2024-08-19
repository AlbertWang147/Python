import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl


#使图表显示中文
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    
mpl.rcParams['axes.unicode_minus'] = False   

#读取文件
study = pd.read_csv('study_information.csv', encoding = 'gbk')
course = study[['user_id' , 'course_id']].groupby('course_id').count()

#得到最多最少人数
Qmin = course['user_id'].values.min()
Qmax = course['user_id'].values.max()

#欢迎度计算函数
def popular_degree(Qi):
    return (Qi-Qmin)/(Qmax-Qmin)

#计算欢迎度
popular = pd.DataFrame(columns = ['course_id', 'number', 'popularity'])
popular['course_id'] = course['user_id'].keys()
popular['number'] = course['user_id'].values
popular['popularity'] = popular['number'].apply(lambda x:popular_degree(x))
popular = popular.sort_values(['popularity'],ascending = False)
p = popular.head(10)

#画图
plt.bar(p['course_id'],p['popularity'])
plt.show()

