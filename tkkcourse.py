#!/usr/bin/python

import re
from bs4 import BeautifulSoup
from tkktools import *

course_name = re.compile(r'([^(^)]+)\(')
course_grade = re.compile(r'\([a-zA-Z]+\)')
course_section = re.compile(r'\)([^(^)]+)\(')
course_nweek = re.compile(r'[单双每]')
course_digital = re.compile(r'[0-9]+')

class Tkk_course:
    #cname, teacher, iroom = 0, 0, 0
    #room = list()
    #isrun = [-1 for i in range(20)]

    def __init__(self):
        self.cname, self.teacher, self.iroom = 0, 0, 0
        self.room = list()
        self.isrun = [-1 for i in range(20)]

    def __repr__(self):
        tt = dict()
        tt['cname'] = self.cname
        tt['teacher'] = self.teacher
        tt['room'] = self.room
        tt['isrun'] = self.isrun
        return str(tt)

    # init tkk_course
    # lcourse is a list 
    #    0: name | 1: teacher | 2: position | 3: rweek regoin
    def format_tcourse(self, lcourse):
        #TESTING init
        #self.isrun = [-1 for i in range(20)]
        #self.room = list()

        self.teacher = lcourse[1]
        self.room.append(lcourse[2])
        # get week region
        rweek = [ int(x) for x in course_digital.findall(lcourse[3]) ]
        nweek = "".join(course_nweek.findall(lcourse[3]))
        self.set_isrun(rweek, nweek2int(nweek), self.iroom)
        self.set_cname(lcourse[0])

    def add_tcourse(self, lcourse):
        if lcourse[2] in self.room:
            idx = self.room.index(lcourse[2])
        else:
            self.room.append(lcourse[2])
            self.iroom += 1
            idx = self.iroom
        rweek = [ int(x) for x in course_digital.findall(lcourse[3]) ]
        nweek = "".join(course_nweek.findall(lcourse[3]))
        self.set_isrun(rweek, nweek2int(nweek), idx)

    def set_cname(self, cc):
        concat = lambda x: str(x[0]) if len(x) else ""
        cname = ""
        cname += concat(course_name.findall(cc))
        cname += concat(course_grade.findall(cc))
        cname += concat(course_section.findall(cc))
        self.cname = cc

    def set_isrun(self, rweek, flg, idx):
        for i in range(rweek[0],rweek[1]+1):
            self.isrun[i] = idx if ( flg == 2 or i%2 ==flg ) else 0

    #def stop_tcourse(self, lcourse):

class Tkk_schedule:
    #tsch = [[0 for i in range(15)] for i in range(10)]
    #viscrs = [[0 for i in range(15)] for i in range(10)]
    #html_str = open("./cschedule.html", "r", encoding='utf-8')
    #wk_cols = list()
    #soup = 0

    def __init__(self):
        self.tsch = [[dict() for i in range(10)] for i in range(10)]
        self.ctime = [list() for i in range(10)]
        self.viscrs = [[list() for i in range(10)] for i in range(10)]
        self.wk_cols = list()
        self.html_str = open("./cschedule.html", "r", encoding='utf-8')
        self.soup = BeautifulSoup(self.html_str, 'html.parser')

    #def add_tcourse(self):

    def init_wkcols(self):
        all_td = self.soup.find_all('th', colspan=course_digital)
        for nums in all_td:
            self.wk_cols.append(int(nums['colspan']))
        for i in range(1, len(self.wk_cols)):
            self.wk_cols[i] += self.wk_cols[i-1]
        self.wk_cols.append(100)

    #TODO:
    #def init_nthc2time(self):

    def generate_schedule(self):
        all_tr = self.soup.find_all('tr', class_= [ 'odd', 'even' ])

        self.init_wkcols()

        # kill sec-11
        for yy, nth_course in zip(range(len(all_tr)-1), all_tr):
            #if nth_course['class'] == ['even']:
            #print(rsp)
            y = int(yy/2)
            nth = 0;
            for i, bet_course in zip(range(len(nth_course)), nth_course):
                #s = list2str((e.text).split())
                tcourse = course2list(str(bet_course))
                jcourse = list2str(tcourse)
                # which week[0-6]
                while i > self.wk_cols[nth]:
                    nth += 1

                # i==0 means time region
                if not i:
                    tdivide = course_digital.findall(tcourse[1])
                    cbegin = tdivide[0]+tdivide[1]
                    cend = tdivide[2]+tdivide[3]
                    tcomb = [cbegin, cend]
                    self.ctime[y].append(tcomb)
                    print(self.ctime)
                elif len(jcourse):
                    x = nth + 1
                    tt = Tkk_course()
                    tt.format_tcourse(tcourse)
                    #print([x, y])
                    #print(tt)
                    if tt.cname in self.viscrs[x][y]:
                        self.tsch[x][y][tt.cname].add_tcourse(tcourse)
                    else:
                        self.viscrs[x][y].append(tt.cname)
                        self.tsch[x][y][tt.cname] = tt
                    #if tmp.cname not in viscrs[x][y]:
                    #    viscrs[x][y].append(tmp.cname)
                    #    tsch[x][y].append(tmp)
                    #attrs = ['课程名', '教师', '地点', '时间段']
                    #print(tcourse)
                    #display = dict(zip(attrs, tcourse))
                    #rweek = rtime = course_digital.findall(tcourse[3])
                    ##print('[起始周, 结束周] =',rweek)
                    #display['时间段'] = rweek
                    #concat = lambda x: str(x[0]) if len(x) else ""
                    #cc = ""
                    #tmp = course_name.findall(tcourse[0])
                    ##cc += get_listfirst(tmp)
                    #cc += concat(tmp)
                    #tmp = course_grade.findall(tcourse[0])
                    #cc += concat(tmp)
                    ##cc += get_listfirst(tmp)
                    #tmp = course_section.findall(tcourse[0])
                    #cc += concat(tmp)
                    ##cc += get_listfirst(tmp)
                    ##print("week = %d \t |  course_findall \t%02d" % (nth+1, i), cc)
                    #display['课程名'] = cc
                    #display['星期'] = nth+1
            #print('--------------------------------------------------------------------------------')

        for x in range(1, 8):
            for y in range(0, 6):
                print('week = %d nth_course = %d' % (x, y+1))
                print(self.tsch[x][y])
            print('--------------------------------------------------------------------------------')
