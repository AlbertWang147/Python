import pandas as pd
import numpy as np

login = pd.read_csv("login.csv",encoding = "gbk")
study = pd.read_csv("study_information.csv",encoding = "gbk")
user = pd.read_csv("users.csv",encoding = "gbk")

#重复值缺失值
print(login.isnull().sum())
print(login.duplicated().sum())
print(study.isnull().sum())
print(study.duplicated().sum())
print(user.isnull().sum())
print(user.duplicated().sum())

user = user.drop_duplicates()
study = study.dropna(subset=["price"])
user['school'] = user['school'].fillna('unknown')

login.to_csv("task1_1_1.csv")
study.to_csv("task1_1_2.csv")
user.to_csv("task1_1_3.csv")

#1.2	recently_logged 字段处理
rl = user[user["recently_logged"] == '--']
print(rl)
print(rl.count())

#将学习时间为0的用户最近登陆时间改为注册时间
dif = user['recently_logged'] == '--'
dif2 = user['learn_time'] == "0"
dif3 = dif&dif2

user.loc[dif3,'recently_logged'] = user.loc[dif3,'register_time']
print(user[user.recently_logged == '--'].count())

#将所有最近登陆时间为--的用户改为注册时间
ind = user['recently_logged'] == '--'

user.loc[ind, 'recently_logged'] = user.loc[ind, 'register_time']

user.to_csv("task1_2.csv")
