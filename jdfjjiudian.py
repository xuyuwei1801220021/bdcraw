#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-04-22 15:05:43
# Project: fjjdtable


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
        self.start = 0;
        
        if response.doc('a[onclick*="last"]').text()=="":
            self.denum=1
        else:
            self.denum =re.findall(r"\d+\.?\d*",response.doc('a[onclick*="last"]').text())[0]
        self.deurls = response.url.partition("https://")[2].partition("-Activities")[0][:]
        self.deurle = response.url.partition("-Activities")[2].partition(".html")[0][:]
        while self.start < int(self.denum):
            self.crawl("https://"+self.deurls+"-Activities-oa"+str(self.start*30)+"-"+self.deurle+".html", callback=self.detail01_page,fetch_type='js')
            self.start+=1;
        
    def detail01_page(self,response):
        for each in response.doc('.listing_details .listing_title a').items():
            self.crawl(each.attr.href, callback=self.detail02_page,fetch_type='js')
    def detail02_page(self, response):
        list = response.doc('[name~=description]').attr("content")
        string = response.doc('[name~=location]').attr("content")
        id = response.url
        list2 =(list.partition("景点，")[2].partition("篇"))[0][:]
        list =[]
        for each in response.doc('div[onclick*=hotel]').text():
            list.append(each)
        
        return{
                "jdid":"d"+response.url.partition("-d")[2].partition("-Reviews")[0][:],
                "fjjd":response.doc('div[onclick*=hotel]').text(),
            }
    
    
   
