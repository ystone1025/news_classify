# -*- coding: utf-8 -*-

import os
import scws
import csv
import re
from svmutil import *

SCWS_ENCODING = 'utf-8'
SCWS_RULES = '/usr/local/scws/etc/rules.utf8.ini'
CHS_DICT_PATH = '/usr/local/scws/etc/dict.utf8.xdb'
CHT_DICT_PATH = '/usr/local/scws/etc/dict_cht.utf8.xdb'
IGNORE_PUNCTUATION = 1

ABSOLUTE_DICT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), './dict'))
CUSTOM_DICT_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'userdic.txt')
EXTRA_STOPWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'stopword.txt')
EXTRA_EMOTIONWORD_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'emotionlist.txt')
EXTRA_ONE_WORD_WHITE_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'one_word_white_list.txt')
EXTRA_BLACK_LIST_PATH = os.path.join(ABSOLUTE_DICT_PATH, 'black.txt')

cx_dict = ['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@']

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_ONE_WORD_WHITE_LIST_PATH)]
    return one_words

def load_black_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
single_word_whitelist |= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')


def load_scws():
    s = scws.Scws()
    s.set_charset(SCWS_ENCODING)

    s.set_dict(CHS_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CHT_DICT_PATH, scws.XDICT_MEM)
    s.add_dict(CUSTOM_DICT_PATH, scws.XDICT_TXT)

    # 把停用词全部拆成单字，再过滤掉单字，以达到去除停用词的目的
    s.add_dict(EXTRA_STOPWORD_PATH, scws.XDICT_TXT)
    # 即基于表情表对表情进行分词，必要的时候在返回结果处或后剔除
    s.add_dict(EXTRA_EMOTIONWORD_PATH, scws.XDICT_TXT)

    s.set_rules(SCWS_RULES)
    s.set_ignore(IGNORE_PUNCTUATION)
    return s

def train_data(flag,weibo,weibo_dict):#词频词网

    black = load_black_words()
    sw = load_scws()
    items = []
    label = []
    word_item = []#分词得到的词语
    for i in range(0,len(weibo)):
        mid = weibo[i]
        text = weibo_dict[weibo[i]][0]
        label.append(weibo_dict[weibo[i]][1])
        words = sw.participle(text)
        row = []
        for word in words:
            if (word[1] in cx_dict) and (3 < len(word[0]) < 30 or word[0] in single_word_whitelist) and (word[0] not in black):#选择分词结果的名词、动词、形容词，并去掉单个词
                row.append(word[0])
                if word[0] not in word_item:
                    word_item.append(word[0])
        items.append(row)

    with open('./svm/train%s.txt' % flag, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(items)):
            row = []
            f_items = '' + str(label[i])
            item = items[i]
            for k in range(0,len(word_item)):
                if word_item[k] in item:
                    f_items = f_items + ' ' + str(k+1) + ':' + str(weibo_dict[weibo[i]][0].count(word_item[k]))
            row.append(f_items)
            writer.writerow((row))

    with open('./svm/feature%s.csv' % flag, 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,len(word_item)):
            writer.writerow(([word_item[i],i+1]))

def start(flag):
    weibo_dict = dict()
    weibo = []
    reader = csv.reader(file('./traing/train%s.csv' % flag, 'rb'))
    for mid,text,label in reader:
        weibo.append(mid)
        weibo_dict[mid] = [text,label]
    
    train_data(flag,weibo,weibo_dict)    

if __name__ == '__main__':
    start('20150124')#生成训练集
