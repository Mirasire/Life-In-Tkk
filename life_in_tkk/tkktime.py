#!/usr/bin/python

import re
import time
import requests
from bs4 import BeautifulSoup

#by mirasire 
from .tkktools import week2int

#
# tkk_time means the standed time from tkk
#
class Tkk_time:


    def __init__(self):
        self.week=""
        self.nthweek=""
        self.year=""
        self.month=""
        self.day=""
        self.home_page = "http://jw.xujc.com/"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
                        "AppleWebKit/537.36 (KHTML, like Gecko)"
                        "Chrome/59.0.3071.115 Safari/537.36"
        }
        self.parse() 

    def __get_index(self):
        return requests.get(self.home_page, headers=self.header)

    def __repr__(self):
        key = ["year", "month", "day", "week", "nthweek"]
        value = [self.year, self.month, self.day, self.week, self.nthweek]
        return str(dict(zip(key, value)))

    def parse(self):
        digital_pattern = re.compile(r'[0-9]+')
        td_pattern = re.compile(r'<td>([^\n]+)</td>')
        # requests tkk_home_page
        index_html = self.__get_index().text
        soup_data = BeautifulSoup(index_html, 'html.parser')
        otkk_data = soup_data.find_all('script')
        tkk_data = td_pattern.findall("".join(otkk_data[0].contents))
        # analyse
        yymm = digital_pattern.findall(tkk_data[0])
        day  = tkk_data[1]
        week = week2int(tkk_data[2])
        nthweek = digital_pattern.findall(tkk_data[3])
        ## package
        self.year = int(yymm[0])
        self.month = int(yymm[1])
        self.day = int(day)
        self.week = int(week)
        self.nthweek = int(nthweek[0])
