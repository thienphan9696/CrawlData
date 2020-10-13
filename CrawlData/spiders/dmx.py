# -*- coding: utf-8 -*-
import scrapy
import cookies
import json
import time
import os

from scrapy.http import Request

class ResponseItem(scrapy.Item):
    link = scrapy.Field()
    progress = scrapy.Field()

class DMXs(scrapy.Spider):
    name = 'linkProDmx'
    z = 0
    final_urls = []
    start_time = time.time()
    def start_requests(self):
        
        # Run for page
        file_link = './output/output_link_dmx_{}.json'.format(self.para)
        
        data = json.load(open(file_link))                                      # Đọc file, Chuyển json --> List để lấy url

        for da in data:
            self.final_urls.append(da['link'])

        x = 0
        y = len(self.final_urls)
        for base_url in self.final_urls:
            x += 1
            self.z = x*100/y
            # time.sleep(0.1)
            self.begin_request_time = time.time()
            yield scrapy.Request(
                                base_url + '?ClearCache=1',
                                # base_url.replace('https://www.thegioididong.com/','https://staging.thegioididong.com/')+ '?ClearCache=1',
                                cookies = {'api': 'java'},
                                headers = {'User-Agent': 'PostmanRuntime'},
                                callback = self.parse, errback = self.error_function)

    
    def error_function(self,failure):
        _time = time.time() - self.start_time
        current_time = time.time() - self.begin_request_time
        if _time > 60:
            time1 = int(_time//60)
            time2 = int(_time%60)
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time1}p{time2}s'.format(percent = round(self.z, 2), current_time=round(current_time, 2),time1=time1, time2=time2))
        else:
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time}s'.format(percent = round(self.z, 2),current_time=round(current_time, 2),time = round(time.time()-self.start_time,2)))

    def parse(self, response):
        _time = time.time() - self.start_time
        current_time = time.time() - self.begin_request_time
        if _time > 60:
            time1 = int(_time//60)
            time2 = int(_time%60)
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time1}p{time2}s'.format(percent = round(self.z, 2), current_time=round(current_time, 2),time1=time1, time2=time2))
        else:
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time}s'.format(percent = round(self.z, 2),current_time=round(current_time, 2),time = round(time.time()-self.start_time,2)))