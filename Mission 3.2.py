import numpy as np
import pandas as pd
from itertools import combinations,permutations
from operator import itemgetter

study = pd.read_csv('study_information.csv', encoding = 'gbk')
study['course_id'] = study['course_id'].apply(lambda x:int(x[2:]))

#找到总学习度最高的5名用户
study['learn_process'] = study['learn_process'].apply(lambda x:int(x[6:len(x)-2]))
learn_process_count = study.groupby(by = 'user_id')['learn_process'].agg('sum')
learn_process_count = learn_process_count.sort_values(ascending = False)
print('学习进度最高的5个用户：')
print(learn_process_count.head(5))
user_5 = learn_process_count[0:5].keys()


item_num = study.course_id.nunique()

#转置表
inverted_table = study.groupby(by = 'user_id')['course_id'].agg(list).to_dict()
#矩阵
W = np.zeros((item_num,item_num))

count_course_users_num = study.groupby(by = 'course_id')['user_id'].agg('count').to_dict()
for key,val in inverted_table.items():
    val.sort(reverse = True)
    for per in combinations(val, 2):
        W[per[0] - 1][per[1] - 1] += 1
        W[per[1] - 1][per[0] - 1] += 1
    
for i in range(W.shape[0]):
    for j in range(W.shape[1]):
        W[i][j] /= np.sqrt(count_course_users_num.get(i)*count_course_users_num.get(j))


w_dict = {}
for i in range(W.shape[0]):
    tmp = []
    for index,k in enumerate(W[i]):
        tmp.append((index+1,k))
    w_dict[i+1] = tmp


#计算指定用户与指定课程兴趣
def interest(user_id, course_id,K,w_dict = w_dict):
    interest = 0
    for i in sorted(w_dict[course_id], key = itemgetter(1), reverse=True)[0:K]:
        course_index = i[0]
        simi = i[1]
        if course_index in inverted_table[user_id]:
            interest += simi
    return interest
#计算用户兴趣列表
def get_interest_list(user_id, K = 20, w_dict = w_dict):
    rank = []
    course_id_list = w_dict.keys()
    for course_id in course_id_list:
        if course_id in inverted_table[user_id]:
            continue
        interests = interest(user_id,course_id,K)
        rank.append((course_id,interests))
    return sorted(rank, key = itemgetter(1), reverse=True)

for u in user_5:
    recommend = get_interest_list(u, 20, w_dict)
    recommend = recommend[0:3]
    rec_course = [('课程'+str(i[0])) for i in recommend]
    print("向{0}推荐".format(u))
    print(rec_course)

