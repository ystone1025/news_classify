# -*- coding: utf-8 -*-

import os
import scws
import csv
import re
import json
import random

def main(name_list):#将json转换成csv

    data = []
    for k in range(0,len(name_list)):
        name = name_list[k]
        print name
        f = open(r'./%s.jl' % name, 'r')
        i = 0
        data = []
        for line in f:
            i = i + 1
            if i%1000 == 0:
                print i
            item = json.loads(line.strip())
##            print item
##            break
            data_item = dict()
            data_item['reposts_count'] = item['reposts_count']
            data_item['_id'] = item['_id']
            data_item['name'] = item['name'].encode('utf-8')
            data_item['website_type'] = item['website_type']
            data_item['text'] = item['text'].encode('utf-8')
            data_item['createdate'] = item['createdate'].encode('utf-8')
            data_item['bmiddle_pic'] = item['bmiddle_pic'].encode('utf-8')
            data_item['retweeted_mid'] = item['retweeted_mid']
            data_item['weibourl'] = item['weibourl'].encode('utf-8')
            data_item['source'] = item['source'].encode('utf-8')
            data_item['attitudes_count'] = item['attitudes_count']
            data_item['secondprovinceid'] = item['secondprovinceid']
            data_item['comments_count'] = item['comments_count']
            data_item['user'] = item['user']
            data_item['timestamp'] = item['timestamp']
            data_item['provinceid'] = item['provinceid']
            #data_item['retweeted_uid'] = item['retweeted_uid']
            data_item['geo'] = item['geo'].encode('utf-8')
            data_item['topics'] = item['topics'][0].encode('utf-8')
            data_item['message_type'] = item['message_type']
            data.append(data_item)

        with open('./rubbish/python/news/train_%s.csv' % name, 'wb') as f:
            writer = csv.writer(f)
            for i in range(0,len(data)):
                item = data[i]
                row = [item['_id'],item['name'],item['text'],item['createdate'],item['reposts_count'],item['website_type'],item['bmiddle_pic'],\
                    item['retweeted_mid'],item['weibourl'],item['source'],item['attitudes_count'],item['secondprovinceid'],\
                    item['comments_count'],item['user'],item['timestamp'],item['provinceid'],item['geo'],item['topics'],item['message_type']]
            #print row
                writer.writerow((row))

def cut_weibo(data,name):#根据规则将新闻和评论分开

    news_data = []
    comment_data = []
    for i in range(0,len(data)):
        text = data[i][2]
        l1 = text.find('【')
        l2 = text.find('】')
        row = [data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6],\
                    data[i][7],data[i][8],data[i][9],data[i][10],data[i][11],\
                    data[i][12],data[i][13],data[i][14],data[i][15],data[i][16],data[i][17],\
                    data[i][18]]
        if l1 == -1 and l2 == -1:#评论
            comment_data.append(row)
            continue
        if '【评】' in text:
            comment_data.append(row)
            continue
        if l1 == 0:
            news_data.append(row)
        else:
            comment_data.append(row)
    
    with open('./rubbish/python/news/news_data_%s.csv' % name, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(news_data)):
            writer.writerow((news_data[i]))

    with open('./rubbish/python/news/comment_data_%s.csv' % name, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(comment_data)):
            writer.writerow((comment_data[i]))

def cut_weibo_2(data):#根据规则将新闻和评论分开,返回标签，1表示新闻，0表示非新闻

    label_data = []
    for i in range(0,len(data)):
        text = data[i][1]
        l1 = text.find('【')
        l2 = text.find('】')
        if l1 == -1 and l2 == -1:#评论
            label_data.append('0')
            continue
        if '【评】' in text:
            label_data.append('0')
            continue
        if l1 == 0:
            label_data.append('1')
        else:
            label_data.append('0')
    
    return label_data

def cut_main(name_list):

    for k in range(0,len(name_list)):
        name = name_list[k]
        weibo = []
        reader = csv.reader(file('./rubbish/python/news/train_%s.csv' % name, 'rb'))
        for line in reader:
            row = [line[0],line[1],line[2],line[3],line[4],line[5],line[6],\
                    line[7],line[8],line[9],line[10],line[11],\
                    line[12],line[13],line[14],line[15],line[16],line[17],\
                    line[18]]
            weibo.append(row)
        cut_weibo(weibo,name)

def rand_text(name):#随机抽取样本

    weibo = []
    reader = csv.reader(file('./rubbish/python/news/%s.csv' % name, 'rb'))
    for line in reader:
        r_int = random.randint(1, 10)
        if r_int == 5 and len(weibo) <= 900:
            row = [line[0],line[1],line[2],line[3],line[4],line[5],line[6],\
                    line[7],line[8],line[9],line[10],line[11],\
                    line[12],line[13],line[14],line[15],line[16],line[17],\
                    line[18],line[19]]
            weibo.append(row)

    with open('./rubbish/python/news/rand_news.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(weibo)):
            writer.writerow((weibo[i]))

def test_main(name):#测试数据
    weibo = []
    reader = csv.reader(file('./rubbish/python/news/%s.csv' % name, 'rb'))
    for line in reader:
        row = [line[0],line[1],line[2],line[3],line[4],line[5],line[6],\
                    line[7],line[8],line[9],line[10],line[11],\
                    line[12],line[13],line[14],line[15],line[16],line[17],\
                    line[18]]
        weibo.append(row)
    label = cut_weibo_2(weibo)

    with open('./rubbish/python/news/test_label_%s.txt' % name, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(label)):
            row = []
            row.append(label[i])
            writer.writerow((row))

if __name__ == '__main__':

##    name_list = ['huge','hulian']
##    main(name_list)#将json文件转化成csv文件
##    cut_main(name_list)#生成训练集
##    rand_text('train_news')
    test_main('train_hulian')
