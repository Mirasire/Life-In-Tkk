# -*- coding: utf-8 -*-

#import os, sys
#sys.path.append(os.path.dirname(__file__))

import re
from bs4 import BeautifulSoup

from .tkktime import Tkk_time
from .tkktools import (week2int,
                       course2list,
                       nweek2int,
                       list2str,
                       format_cname,
                       course_name,
                       course_grade,
                       course_section,
                       course_nweek,
                       course_digital,
                       course_rnc,
                       Get_ntime)

from life_in_tkk import tkktools

class Tkk_course:

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

    def __set_cname(self, cc):
        concat = lambda x: str(x[0]) if len(x) else ""
        cname = ""
        cname += concat(course_name.findall(cc))
        cname += concat(course_grade.findall(cc))
        cname += concat(course_section.findall(cc))
        self.cname = cname

    # init tkk_course
    # lcourse is a list 
    #    0: name | 1: teacher | 2: position | 3: rweek regoin
    def format_tcourse(self, lcourse):

        self.teacher = lcourse[1]
        self.room.append(lcourse[2])
        # get week region
        rweek = [ int(x) for x in course_digital.findall(lcourse[3]) ]
        nweek = "".join(course_nweek.findall(lcourse[3]))
        self.set_isrun(rweek, nweek2int(nweek), self.iroom)
        self.__set_cname(lcourse[0])

    def modify_tcourse(self, lcourse):
        if lcourse[2] in self.room:
            idx = self.room.index(lcourse[2])
        else:
            self.room.append(lcourse[2])
            self.iroom += 1
            idx = self.iroom
        rweek = [ int(x) for x in course_digital.findall(lcourse[3]) ]
        nweek = "".join(course_nweek.findall(lcourse[3]))
        self.set_isrun(rweek, nweek2int(nweek), idx)

    def set_isrun(self, rweek, flg, idx):
        for i in range(rweek[0],rweek[1]+1):
            self.isrun[i] = idx if ( flg == 2 or i%2 ==flg ) else 0

    def stop_tcourse(self, iweek):
        self.isrun[iweek] = -1

class Tkk_schedule:

    def __init__(self):
        self.tsch = [[dict() for i in range(10)] for i in range(10)]
        self.ctime = [list() for i in range(10)]
        self.viscrs = [[list() for i in range(10)] for i in range(10)]
        self.wk_cols = list()
        # rnc2y[nth-class] -> index
        self.rnc2y = dict()


    def adjust_schedule(self):
        ## stoped course:
        ##    2: course_name | 4: stop_nthweek | 5: week | 6: same ad y in generate_schedule
        ##    else is trash
        self.__stop_course()
        self.__adjust_course()

    #tcourse formate 0: name | 1: teacher | 2: position | 3: rweek regoin
    def generate_schedule(self, tencode='utf-8'):
        csch_html=tkktools.csch_addr
        cadj_html=tkktools.cadj_addr
        self.csch_str = open(csch_html, "r", encoding=tencode)
        self.csch_soup = BeautifulSoup(self.csch_str, 'html.parser')
        self.cadj_str = open(cadj_html, "r", encoding=tencode)
        self.cadj_soup = BeautifulSoup(self.cadj_str, 'html.parser')
        all_tr = self.csch_soup.find_all('tr', class_= [ 'odd', 'even' ])

        self.__init_wkcols()

        # kill sec-11
        tmp_rnc = ""
        for yy, nth_course in zip(range(len(all_tr)-1), all_tr):
            y = int(yy/2)
            nth = 0;
            for i, bet_course in zip(range(len(nth_course)), nth_course):
                tcourse = course2list(str(bet_course))
                jcourse = list2str(tcourse)
                # which week[0-6]
                while i > self.wk_cols[nth]:
                    nth += 1

                # i==0 means time region
                if not i:
                    # tcomb is the timeline region
                    tdivide = course_digital.findall(tcourse[1])
                    cbegin = tdivide[0]+tdivide[1]
                    cend = tdivide[2]+tdivide[3]
                    tcomb = [cbegin, cend]
                    self.ctime[y].append(tcomb)
                    # ATTENTION-FLAG: MAYBE COURSE BUG HERE
                    if not yy%2:
                        tmp_rnc = course_rnc.findall(tcourse[0])[0]
                    else:
                        tmp_rnc += '-' + course_rnc.findall(tcourse[0])[0]
                        self.rnc2y[tmp_rnc] = y
                elif len(jcourse):
                    x = nth + 1
                    self.__add_course2schedule(x, y, tcourse)

    def __get_course(self, x, y, nwk):
        # Consider Other situation
        re_course = Tkk_course()
        for i, course in enumerate(self.tsch[x][y].values()):
            if course.isrun[nwk] != -1:
                re_course = course
                #print("x = %d | course = %s | type = %s" % (i, str(course), type(course)))
                break

        return re_course

    #def time2end(self):
    #def time2relax(self):

    def is_incourse(self, idx, time):
        return (self.ctime[idx][0][0] <= time)

    def __now_cidx(self, now_time):
        time_tabel = self.ctime
        idx = -1
        for i, tmspan in enumerate(time_tabel):
            print(i, tmspan)
            if(now_time<="0700" or now_time>"2110"):
                break
            elif now_time<=tmspan[-1][-1]:
                #time_rm1 = int(tmspan[0][0]) - int(now_time)
                #time_rm2 = int(tmspan[-1][-1]) - int(now_time)
                idx = i
                break
        return idx

    # TODO: Judge When y = -1
    def reminder(self, tmahead=30):
        print("tmahead = %d" % tmahead)
        tmp_time = Get_ntime()
        jwtime = Tkk_time()
        now_time = "%02d%02d" % (tmp_time.hour, tmp_time.minute)
        # USE FOR DEBUG

        x = jwtime.week
        y = self.__now_cidx(now_time)
        on_class = self.is_incourse(y, now_time)
        y_cnxt = y + 1 if on_class and y != 5 else y
        now_course = self.__get_course(x, y, jwtime.nthweek)
        nxt_course = self.__get_course(x, y_cnxt, jwtime.nthweek)
        print("now_course = ", now_course)
        print("nxt_course = ", nxt_course)

    def display(self):
        for x in range(1, 8):
            for y in range(0, 6):
                print('x=%d, y=%d' % (x, y), end=" | ")
                print(self.tsch[x][y])
            print('----------------------------------------------------------------')

    def get_timetable(self):
        return self.ctime

    def __init_wkcols(self):
        all_td = self.csch_soup.find_all('th', colspan=course_digital)
        for nums in all_td:
            self.wk_cols.append(int(nums['colspan']))
        for i in range(1, len(self.wk_cols)):
            self.wk_cols[i] += self.wk_cols[i-1]
        self.wk_cols.append(100)

    def __stop_course(self):
        stp = self.cadj_soup.find_all('table', id='data_table')
        all_tr = stp[0].find_all('tr', class_=['odd', 'even'])
        for i, ele in zip(range(len(all_tr)), all_tr):
            atd = [ i.text for i in ele.find_all('td') ]
            cname = format_cname(atd[2])
            x = week2int(atd[5])
            y = self.rnc2y[atd[6]]
            iweek = int(atd[4])
            self.tsch[x][y][cname].stop_tcourse(iweek)

    def __adjust_course(self):
        stp = self.cadj_soup.find_all('table', id='data_table2')
        all_tr = stp[0].find_all('tr', class_=['odd', 'even'])
        #tcourse formate 0: name | 1: teacher | 2: position | 3: rweek regoin
        for i, ele in zip(range(len(all_tr)), all_tr):
            atd = [ i.text for i in ele.find_all('td') ]
            cname = format_cname(atd[2])
            tcourse = [atd[2], atd[3], atd[-1], atd[4]+'-'+atd[4]]
            x, y = week2int(atd[5]), self.rnc2y[atd[6]]
            self.__add_course2schedule(x, y, tcourse)

    def __add_course2schedule(self, x, y, tcourse):
        tt = Tkk_course()
        tt.format_tcourse(tcourse)
        if tt.cname in self.viscrs[x][y]:
            self.tsch[x][y][tt.cname].modify_tcourse(tcourse)
        else:
            self.viscrs[x][y].append(tt.cname)
            self.tsch[x][y][tt.cname] = tt
