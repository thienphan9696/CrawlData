# -*- coding: utf-8 -*-
import scrapy
import cookies
import json
import time
import urllib

from scrapy.http import Request


class ResponseItem(scrapy.Item):
    name = scrapy.Field()

class DMX(scrapy.Spider):
    name = 'dmx'

    # custom_settings = {'COOKIES_ENABLED':True, 'COOKIES_DEBUG':True}

    start_time = time.time()
    z = 0
    start_url = 'https://www.dienmayxanh.com/cart/them-vao-gio-hang?ProductId={}&'
    final_ids = []

    getValue = {'productType': 1}

    def start_requests(self):
        
        file_link = './output/output_id_dmx_{}.json'.format(self.id)        
        
        data = json.load(open(file_link))                                       # Đọc file, Chuyển json --> List để lấy url
        for da in data:
            self.final_ids.append(da['link'])

        # provin = '{}/provin.json'.format(path)
        # data_provin = json.load(open(provin))

        y = len(self.final_ids)
        x = 0

        for i in self.final_ids:
            # for ii in data_provin(0, 9):
                x += 1
                self.z = x*100/y
                time.sleep(1)
                self.begin_request_time = time.time()
                yield scrapy.Request(
                                self.start_url.format(i) + urllib.parse.urlencode(self.getValue),
                                # self.start_url.format(i).replace('https://www.thegioididong.com/','https://www.dienmayxanh.com/') + urllib.parse.urlencode(self.getValue),
                                # cookies = {'api': 'java'},
                                # cookies = {'DMX_Personal':'{}'.format(ii)},
                                headers = {'User-Agent': 'PostmanRuntime'},
                                meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                callback = self.parse, errback= self.error_function)

    def error_function(self,failure):
        _time = time.time()-self.start_time
        current_time = time.time()- self.begin_request_time
        if _time > 60:
            time1 = int(_time//60)
            time2 = int(_time%60)
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time1}p{time2}s'.format(percent = round(self.z, 2), current_time=round(current_time, 2),time1=time1, time2=time2))
        else:
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time}s'.format(percent = round(self.z, 2),current_time=round(current_time, 2),time = round(time.time()-self.start_time,2)))

    def parse(self, response):
        _time = time.time()-self.start_time
        current_time = time.time()- self.begin_request_time
        if _time > 60:
            time1 = int(_time//60)
            time2 = int(_time%60)
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time1}p{time2}s'.format(percent = round(self.z, 2), current_time=round(current_time, 2),time1=time1, time2=time2))
        else:
            self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time}s'.format(percent = round(self.z, 2),current_time=round(current_time, 2),time = round(time.time()-self.start_time,2)))
