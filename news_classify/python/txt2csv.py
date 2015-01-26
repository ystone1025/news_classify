# -*- coding: utf-8 -*-

import os
import scws
import csv
import re

def main(name_list):

    data = []
    for k in range(0,len(name_list)):
        name = name_list[k]
        print name
        f = open(r'./traing/%s.txt' % name, 'r')
        i = 0
        data = []
        for line in f:
            if i > 1:
                line =  line.strip('\n')
                if len(line):
                    #print line.split('|***|')
                    mid,text,label = line.split('|***|')
                    #print i,label
                    if str(label) != '2':#去掉无法判断的文本
                        data.append([mid,text,label])
            i = i + 1

    with open('./traing/train.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(data)):
            writer.writerow(([data[i][0],data[i][1],data[i][2]]))

if __name__ == '__main__':

    name_list = ['fanrui_label','fanrui2_label','fengxu_label','liangxiao-label','liruiwen_mark','lisendong_label','wangzhipeng','zhangleihan_tagged','zhaojichang_label']
    main(name_list)#生成训练集
