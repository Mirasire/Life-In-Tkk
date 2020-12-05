# -*- coding: utf-8 -*-

import time
import re
from bs4 import BeautifulSoup

csch_addr = "./cschedule.html"
cadj_addr = "./cadjusted.html"
pic_addr = "./verify.png"

course_name = re.compile(r'([^(^)]+)\(')
course_grade = re.compile(r'\([a-zA-Z]+\)')
course_section = re.compile(r'\)([^(^)]+)\(')
course_nweek = re.compile(r'[单双每]')
course_digital = re.compile(r'[0-9]+')
course_rnc = re.compile(r'[0-9午]+')

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
        "周六" : 6,
        "周日" : 0,
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
    return n2i[nk] if len(nk) != 0 else 2

def format_cname(cc):
    concat = lambda x: str(x[0]) if len(x) else ""
    cname = ""
    cname += concat(course_name.findall(cc))
    cname += concat(course_grade.findall(cc))
    cname += concat(course_section.findall(cc))
    return cname
