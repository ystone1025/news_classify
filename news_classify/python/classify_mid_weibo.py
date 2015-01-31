# -*- coding: utf-8 -*-

import os
import csv
import re
import time

def load_happy():
    happy_list = []
    reader = csv.reader(file('./words/happy.txt', 'rb'))
    for line in reader:
        happy_list.append(line[0])
    return happy_list

def load_angry():
    angry_list = []
    reader = csv.reader(file('./words/angry.txt', 'rb'))
    for line in reader:
        angry_list.append(line[0])
    return angry_list

def load_sad():
    sad_list = []
    reader = csv.reader(file('./words/sad.txt', 'rb'))
    for line in reader:
        sad_list.append(line[0])
    return sad_list

happy = load_happy()
angry = load_angry()
sad = load_sad()

def main(name):#数据输入

    reader = csv.reader(file('./test/weibo%s.csv' % name, 'rb'))
    label_data = []
    for line in reader:
        text = line[2]
        mid = line[0]
        label = mid_sentiment_classify(text)        
        label_data.append([label,mid,text])

    with open('./test/test_weibo_%s.csv' % name, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(label_data)):
            writer.writerow((label_data[i]))

def mid_sentiment_classify(text):#中性情绪再分类

    label = label_classify(text)
    #print label
    if label == -1:
        label = label_adjust(label,text)

    return label 

def label_adjust(label,text):#类别标签调整

    n1 = text.count('！')
    n2 = text.count('？')
    if n1 == 1 and n2 == 0:
        label = 1
    elif n1 == 1 and n2 == 1:
        label = 2#3
    elif n1 > 1:
        label = 2#3
    elif n1 == 0 and n2 > 0:
        label = 2#3
    elif text.find('…') != -1 or text.find('...') != -1:
        label = 3#2
    elif text.find('//@') == 0 or text.find('/@') == 0:
        label = 1
    else:
        label = -1

    return label 


def label_classify(text):#中性文本分类

    happy_count = 0
    angry_count = 0
    sad_count = 0
    for i in range(0,len(happy)):
        if happy[i] in text:
            happy_count = happy_count + 1

    for i in range(0,len(angry)):
        if angry[i] in text:
            angry_count = angry_count + 1

    for i in range(0,len(sad)):
        if sad[i] in text:
            sad_count = sad_count + 1

    happy_count = float(happy_count)/float(len(happy))
    sad_count = float(sad_count)/float(len(sad))
    angry_count = float(angry_count)/float(len(angry))

    if happy_count >= sad_count and happy_count >= angry_count and happy_count != 0:
        return 1
    elif sad_count >= happy_count and sad_count >= angry_count and sad_count != 0:
        return 3#2
    elif angry_count >= happy_count and angry_count >= sad_count and angry_count != 0:
        return 2#3
    else:
        return -1
        

if __name__ == '__main__':
    main('edu0131')
