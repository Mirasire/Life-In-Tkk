#!/usr/bin/python

import time
import re
from bs4 import BeautifulSoup

def w2file(name, data):
    with open(name,"w", encoding='utf-8') as f:
        f.write(data)

def week2int(cweek):
    w2i = {
        "星期一" : 1,
        "星期二" : 2,
        "星期三" : 3,
        "星期四" : 4,
        "星期五" : 5,
        "星期六" : 6,
        "星期日" : 0,
        "周一" : 1,
        "周二" : 2,
        "周三" : 3,
        "周四" : 4,
        "周五" : 5,
    }
    return w2i[cweek]

#TODO
def get_ldate():
    return time.strftime("%Y-%M-%D", time.localtime())

def course2list(course):
    s = course.replace('<br/>', '_')
    soup = BeautifulSoup(s,'html.parser')
    tcourse = re.split('\xa0|_', soup.text)
    return tcourse

def list2str(target):
    restr = ""
    for i in target:
        restr += str(i)
    return restr

def nweek2int(nk):
    n2i = {
        "双" : 0,
        "单" : 1,
        "每" : 2,
    }
    return n2i[nk]
