'''
Created on Jan 22, 2018

@author: yingjie
'''


# import os
# 
# 
# city_name_dict = dict()
# max_len = 0
# count = 0
# for fname in os.listdir('../city_poi_data'):
#     for line in open(os.path.join('../city_poi_data', fname)):
#         splitted = line.split()
#         count+=1
#         city_name_dict[splitted[0].strip()] = 0
#         poi_name_len = len(splitted)-1
#         if poi_name_len > max_len:
#             max_len = poi_name_len
#             
# print(max_len)
# 
# print(max_len/(count*1.0))
import operator

a = [5,3,1,4,10]

print(sorted(range(len(a)), key=lambda i: a[i])[-2:])

print(zip(*sorted(enumerate(a), key=operator.itemgetter(1)))[0][-2:])

