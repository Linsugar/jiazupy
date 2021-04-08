from django.test import TestCase

# Create your tests here.
# s1=  '1324324'
# print(s1[-1:3:-1])

from functools import reduce
# 定义函数
# def f(x,y):
#     return x+y
# # 定义序列，含1~100的元素
# items = range(1,100)
# # 使用reduce方法
# result = reduce(f,items)
# print(result)
l1= [12,2,34]
def f(x):
    print(x)
print(filter(f,l1))
import random
print(random.randint(1000000000,80000000000))