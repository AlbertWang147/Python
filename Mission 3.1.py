import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl


mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']    
mpl.rcParams['axes.unicode_minus'] = False   

study = pd.read_csv('study_information.csv', encoding = 'gbk')
course = study[['user_id' , 'course_id']].groupby('course_id').count()

Qmin = course['user_id'].values.min()
Qmax = course['user_id'].values.max()

def popular_degree(Qi):
    return (Qi-Qmin)/(Qmax-Qmin)

#计算欢迎度
popular = pd.DataFrame(columns = ['course_id', 'number', 'popularity'])
popular['course_id'] = course['user_id'].keys()
popular['number'] = course['user_id'].values
popular['popularity'] = popular['number'].apply(lambda x:popular_degree(x))
popular = popular.sort_values(['popularity'],ascending = False)
p = popular.head(10)

plt.bar(p['course_id'],p['popularity'])
plt.show()
