# -*- coding: utf-8 -*-

import os
import sys
import time
import pytesseract
import traceback
import numpy as np
from selenium import webdriver
from PIL import Image
from bs4 import BeautifulSoup
##if wanna secret the input passwd
#from getpass import getpass

sys.path.append(os.path.dirname(__file__))

#by mirasire
from .tkktools import (week2int,
                       w2file,
                       course2list,
                       nweek2int,
                       list2str,
                       format_cname)

from life_in_tkk import tkktools

#
# get schedule html && adjusted course infomation
#
class Tkk_html:

    def __init__(self):
        self.option, self.firefox = 0, 0
        self.url = "http://jw.xujc.com"
        self.img, self.width, self.height = 0, 0, 0
        self.vis, self.stp, self.maze = 0, 0, 0
        self.user, self.passwd = 0, 0
        self.vercode = 0
        self.dic = {}
        self.fset = set()

    def start_firefox(self):
        self.option = webdriver.FirefoxOptions()
        self.option.add_argument('-headless')
        self.firefox = webdriver.Firefox(options=self.option);

    def set_login(self, user, passwd):
        self.user = user
        self.passwd = passwd

    def login2jw(self, user, passwd):
        flg = 1
        self.start_firefox()
        ## make sure [ user && passwd ] is correct
        self.set_login(user, passwd)
        while flg:
            self.identify_image()
            #print(self.vercode)
            self.firefox.find_element_by_id('username').clear()
            self.firefox.find_element_by_id('username').send_keys(self.user)
            self.firefox.find_element_by_id('password').clear()
            self.firefox.find_element_by_id('password').send_keys(self.passwd)
            self.firefox.find_element_by_id('imgcode').clear()
            self.firefox.find_element_by_id('imgcode').send_keys(self.vercode)
            self.firefox.find_element_by_id('loginbtn').click()
            flg = self.get_html()
        self.firefox.quit()

    def gb2utf8(self, odata):
        soup = BeautifulSoup(odata,'html.parser')
        soup.encoding = 'utf-8'
        return str(soup)

    def get_html(self):
        try:
            self.firefox.find_element_by_link_text('常用链接').click()
            time.sleep(1)
            self.firefox.find_element_by_link_text('课程表').click()
            w2file(tkktools.csch_addr, self.gb2utf8(self.firefox.page_source))
            self.firefox.find_element_by_link_text('常用链接').click()
            time.sleep(1)
            self.firefox.find_element_by_link_text('调停补课信息').click()
            w2file(tkktools.cadj_addr, self.gb2utf8(self.firefox.page_source))
        except Exception as e:
            print(str(e))
            return int(1)
        return int(0)

    # return string
    def pixel2hex(self, pix):
        thex = ""
        for i in pix:
            thex += str("%02x" % (i))
        return thex

    # return tuple
    def hhex2pixel(self, hhex):
        pix = list()
        flg = 0
        thex = ""
        for i in hhex:
            flg += 1
            thex += i
            if flg%2 == 0:
                pix.append(int("0x%s" % thex, 0))
                thex = ""
        return tuple(pix)

    def dfs_ck(self, x, y):
        return ( x >= 0 and x < self.height and y >= 0 and y < self.width and (not self.vis[x][y]))

    def dfs(self, x, y, key):
        self.vis[x][y] = 1
        for i in range(4):
            nx = x + self.stp[i][0]
            ny = y + self.stp[i][1]
            if (self.dfs_ck(nx, ny)) and (key == self.maze[nx][ny]):
                self.dfs(nx, ny, key)

    def clear_image(self):
        for x in range(0, self.height):
            for y in range(0, self.width):
                key = self.maze[x][y]
                if not self.vis[x][y]:
                    self.dic[key] = (self.dic[key] + 1) if (key in self.dic) else 1
                    self.dfs(x, y, key)

    def identify_image(self):
        self.firefox.get(self.url)
        png = self.firefox.find_element_by_id('img')
        png.screenshot(tkktools.pic_addr)
        img = self.img = Image.open(tkktools.pic_addr)

        # set width and height
        width = self.width = img.width
        height = self.height = img.height

        # set for clear the nose point
        self.vis = np.zeros((height, width), dtype=int)
        self.stp = np.array([[1,0],[0,1],[-1,0],[0,-1]])
        self.maze = np.full((height, width), "ffffffff", dtype=np.dtype('U8'))

        for x in range(0,height):
            for y in range(0,width):
                pix = img.getpixel((y,x))
                key = self.pixel2hex(pix) if ( x != 0 and y != 0) else "ffffffff"
                self.maze[x][y] = key

        self.clear_image()
        dic_st = sorted(self.dic.items(), key= lambda _itm:(_itm[1],_itm[0]))

        for x in range(1, height):
            for y in range(1, width):
                pix = img.getpixel((y, x))
                pix = (255, 255, 255, 255) if (self.pixel2hex(pix) == dic_st[-1][0]) else pix
                self.img.putpixel((y,x), pix)

        #img.save('kill.png')

        # convert to white/black
        img = img.convert('L')
        limite = 165
        table = []
        for i in range(256):
            table.append(0 if i < limite else 1)

        img = img.point(table, '1')
        #img.save('gray.png')

        # cut into 4 pieces
        wh = int(width/4)
        self.vercode = ""
        for i in range(4):
            box = (wh*i, 0, wh*(i+1), height)
            region = img.crop(box)
            tmp = pytesseract.image_to_string(region, lang='eng', \
                                            config="--psm 10 --oem 1 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVvWXYZ")
            self.vercode += tmp[0]
