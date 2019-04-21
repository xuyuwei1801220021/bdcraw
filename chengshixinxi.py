#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-04-21 18:08:13
# Project: xuexi

from pyspider.libs.base_handler import *
import re



class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.page = 0
        self.totalpages = 45
        self.num = 50
        self.urlstart = "https://www.tripadvisor.cn/Attractions-g294211-Activities-oa"
        self.urlend = "-China.html"
        
        
    @every(minutes=24 * 60)
    def on_start(self):
        while self.page<self.totalpages:
            self.crawl(self.urlstart+str(20+self.num*self.page)+self.urlend, callback=self.index_page,fetch_type='js')
            self.page +=1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#LOCATION_LIST .geoList li a').items():
            self.crawl(each.attr.href, callback=self.detail_page,fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        list = response.doc('[name~=description]').attr("content")
        string = response.doc('[name~=location]').attr("content")
        id = response.url
        list2 =(list.partition("景点，")[2].partition("篇"))[0][:]
        #TripAdvisor(猫途鹰)，大连旅游景点，322处大连景点，8,476篇大连景点点评，来自千万用户的大连景点信息和亲身体验，让你尽兴游玩大连景点。满铁本社旧址，森林动物园，海之韵公园...玩在大连，留下点评。
        return {
            "csid": (id.partition("Attractions-")[2].partition("-Activities"))[0][:],
            "csname": (string.partition("province=")[2].partition(";city="))[0][:],
            "sfname": (string.partition(";city=")[2].partition(";coord="))[0][:],
            "jdnum ": (list.partition("旅游景点，")[2].partition("处"))[0][:],
            "dpnum ": (list2.partition("景点，")[2].partition("篇"))[0][:],
        }
   
