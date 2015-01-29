# -*- coding: utf-8 -*-

#  gathering snmp data
from __future__ import division
import os
import datetime
import random
import time
import nltk
import re
from gensim import corpora, models, similarities
import string
import scws

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

def load_one_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_ONE_WORD_WHITE_LIST_PATH)]
    return one_words

def load_black_words():
    one_words = [line.strip('\r\n') for line in file(EXTRA_BLACK_LIST_PATH)]
    return one_words

single_word_whitelist = set(load_one_words())
single_word_whitelist |= set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
cut_str = load_scws()

def cut(s, text, f=None, cx=False):
    if f:
        tks = [token for token
               in s.participle(cut_filter(text))
               if token[1] in f and (3 < len(token[0]) < 30 or token[0] in single_word_whitelist)]
    else:
        tks = [token for token
               in s.participle(cut_filter(text))
               if 3 < len(token[0]) < 30 or token[0] in single_word_whitelist]

    if cx:
        return tks
    else:
        return [tk[0] for tk in tks]

def cut_filter(text):
    pattern_list = [r'\（分享自 .*\）', r'http://\w*']
    for i in pattern_list:
        p = re.compile(i)
        text = p.sub('', text)
    return text

def remove_at(text):
    """text去除@
       text: utf-8
    """
    at_pattern = r'\/\/@(.+?):'
    #text = text + ' ' # 在每个input后加一个空格，以去掉@在末尾的情况
    text = re.sub(at_pattern, '。', text)
    #text = text.strip()

    return text

def emoticon(pe_set, ne_set, text):
    """ Extract emoticons and define the overall sentiment"""

    emotion_pattern = r'\[(\S+?)\]'
    remotions = re.findall(emotion_pattern, text)
    p = 0
    n = 0

    if remotions:
        for e in remotions:
            if e in pe_set:
                p = 1
            elif e in ne_set:
                n = 1

    state = 0
    if p == 1 and n == 0:
        state = 1
    elif p == 0 and n == 1:
        state = 2


    return state

'''define 2 kinds of seed emoticons'''
pe_set = set([])
ne_set = set([])
with open('./sentiment/emoticons4conflict.txt') as f:
    for l in f:
        pair = l.rstrip().split(':')
        if pair[1] == '1':
            pe_set.add(pair[0])
        else:
            ne_set.add(pair[0])
print 'emoticons,p_set,n_set:',len(pe_set),len(ne_set)

'''define subjective dictionary and subjective words weight'''
dictionary_1 =corpora.Dictionary.load('./sentiment/subjective_54W_4.dict')
step1_score = {}
with open('./sentiment/new_emoticon_54W_4.txt') as f:
    for l in f:
        lis = l.rstrip().split()
        step1_score[int(lis[0])] = [float(lis[1]),float(lis[2])]


def triple_classifier(tweet):
    sentiment = 0
    text = tweet
    
    if '//@' in text:
        text = text[:text.index('//@')]
    if not len(text):
        text = remove_at(tweet)
    emoticon_sentiment = emoticon(pe_set,ne_set, text)
    if emoticon_sentiment in [1,2]:
        sentiment = 1
        text = ''       

    if text != '':
        entries = cut(cut_str, text)
        entry = [e.decode('utf-8') for e in entries]
        bow = dictionary_1.doc2bow(entry)
        s = [1,1]
        for pair in bow:
            s[0] = s[0] * (step1_score[pair[0]][0] ** pair[1])
            s[1] = s[1] * (step1_score[pair[0]][1] ** pair[1])
        if s[0] <= s[1]:
            sentiment = 1
        else:
            sentiment = 0

    return sentiment


if __name__ == '__main__':
    text = remove_at('//@王振宇律师: //@三圣临朝你幸福吗://@文山娃:副局长叫冯志明，王，徐两位律师代理的杜文案，以及 @王振宇律师 代理的呼格案再审，冯均为案件关联人 //@李和平律师:局长是谁？他应对骚扰负责//@徐昕:还没查到我这里呀，吓死了 //@文山娃: //@王甫律师:这是第一次遭遇警察查房，而且是白天。太巧了！')
    print text
