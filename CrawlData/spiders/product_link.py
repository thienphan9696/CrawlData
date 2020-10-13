# -*- coding: utf-8 -*-
import scrapy
import urllib
import cookies
import os
import time

from scrapy.http import Request

class ResponseItem(scrapy.Item):
    link = scrapy.Field()
#     id_pro=scrapy.Field()

class TabletSpiders(scrapy.Spider):
        name = 'TGDD'      
        Cate = 0                        # -1: Ngành hàng điện thoại, Laptop,... 
                                        # 1: Phụ kiện
                                        # 0: All
        flag = False

        domain = 'https://www.thegioididong.com'

        param = 'aj/CategoryV6/Product'

        param_phukien = 'aj/AccessoryV4/Product'

        #Truyền tham số
        getValue = {'ClearCache':'1',                                 #dtdd, laptop, tablet, donghothongminh
                'Manufacture':'0',
                'PriceRange':'0',
                'Feature':'0',
                'Property':'0',
                'OrderBy':'0',
                'PageSize':'30',
                'FeatureProduct':'2',
                'Others':'',
                }

        getValue_phukien = {'ClearCache':'1',
                'Product':'0',                                         
                'Size':'20',
                'Property':'',
                'Range':'0',
                'Sale':'0',
                'Manu':'0',
                'Manus':'0',
                'Order':'3',
                'Genuine':'0'
                }

        def start_requests(self):
                final_urls=[]
                _urls = [
                        ['{domain}/{param}?Category=42&&PageIndex={index}&',6],         #Điện thoại di dộng
                        ['{domain}/{param}?Category=44&PageIndex={index}&',2],          #Laptop
                        ['{domain}/{param}?Category=522&PageIndex={index}&',1],
                        ['{domain}/{param}?Category=7264&PageIndex={index}&', 200],           #Đồng hồ thời trang nam
                        ['{domain}/{param}?Category=7077&PageIndex={index}&',3],              #Đồng hồ thông minh     
                ]
                _urls_phukien = [                        
                        ['{domain}/{param}?Category=57&Index={index}&',3],              #Pin sạc dự phòng
                        ['{domain}/{param}?Category=58&Index={index}&',12],             #Sạc, cáp
                        ['{domain}/{param}?Category=54&Index={index}&',7],              #Tai nghe
                        ['{domain}/{param}?Category=2162&Index={index}&',4],            #Loa
                        ['{domain}/{param}?Category=55&Index={index}&',1],              #Thẻ nhớ 
                        ['{domain}/{param}?Category=75&Index={index}&',1],              #USB
                        ['{domain}/{param}?Category=1902&Index={index}&',1],            #Ổ cứng di động
                        ['{domain}/{param}?Category=0&Index={index}&Brand=999&',14],    #Phụ kiện chính hãng
                        ['{domain}/{param}?Category=86&Index={index}&',2],              #Chuột máy tính
                        ['{domain}/{param}?Category=1363&Index={index}&',11],           #Miếng dán màn hình
                        ['{domain}/{param}?Category=60&Index={index}&',81],             #Ốp lưng điện thoại
                        ['{domain}/{param}?Category=1662&Index={index}&',1],            #Ốp lưng máy tính bảng
                        ['{domain}/{param}?Category=7923&Index={index}&',1],            #Balo, tui chống sốc
                        ['{domain}/{param}?Category=4728&Index={index}&',1],            #Camera giám sát, hành trình
                        ['{domain}/{param}?Category=4727&Index={index}&',2],            #Thiết bị mạng, android TV box
                        ['{domain}/{param}?Category=9041&Index={index}&',1],            #Phụ kiện ô tô
                        ['{domain}/{param}?Category=7922&Index={index}&',1],            #Quạt mini
                        ['{domain}/{param}?Category=3885&Index={index}&',1],            #Gậy tự sướng
                        ['{domain}/{param}?Category=6862&Index={index}&',1],            #Giá đỡ laptop, điện thoại
                        ['{domain}/{param}?Category=7924&Index={index}&',2],            #Đế, móc điện thoại
                        ['{domain}/{param}?Category=56&Index={index}&',1],              #Pin tiểu, pin điện thoại
                        ['{domain}/{param}?Category=7925&Index={index}&',2],            #Túi dựng Airpods
                        ['{domain}/{param}?Category=6859&Index={index}&',1],            #Túi chống nước
                        ['{domain}/{param}?Category=6858&Index={index}&',1],            #Miếng lót bàn phím
                        ['{domain}/{param}?Category=1882&Index={index}&',1],            #Phụ kiện Ipad  
                        ['{domain}/{param}?Category=85&Index={index}&',1],              #Phần mềm
                        ['{domain}/{param}?Category=5697&Index={index}&',1],            #Máy tính bộ - Màn hình
                        ['{domain}/{param}?Category=5698&Index={index}&',1],
                        ['{domain}/{param}?Category=5693&Index={index}&',1],            #Mực in - Máy in
                        ['{domain}/{param}?Category=1262&Index={index}&',1],
                ]

                if self.Cate == 0:
                        self.flag = True
                
                if self.Cate == (0 if self.flag else -1):
                        for url in _urls:
                                url[0] = url[0].format(domain = self.domain, param = self.param, index = '{}') + urllib.parse.urlencode(self.getValue)
                        final_urls.extend(_urls)
                if self.Cate == (0 if self.flag else 1):
                        for url in _urls_phukien:
                                url[0] = url[0].format(domain = self.domain, param = self.param_phukien, index = '{}') + urllib.parse.urlencode(self.getValue_phukien)
                        final_urls.extend(_urls_phukien)
                
                x = 0
                y = 0
                flag = True
                for base_url in final_urls:
                        y += base_url[1]

                if hasattr(self, 'cate'):
                        for base_url in final_urls:
                                if base_url[0].find('{}'.format(self.cate)) > -1:
                                        for index in range(base_url[1]):
                                                x += 1
                                                self.z = x*100/y
                                                # time.sleep(1)
                                                url = base_url[0].format(index)
                                                yield scrapy.Request(url,
                                                                cookies = {'api':'java'},
                                                                headers = {'User-Agent':'PostmanRuntime'},
                                                                callback = self.parse, errback = self.error_function)
                                        flag = False
                                        break
                if flag:
                    for base_url in final_urls:
                        for index in range(base_url[1]):
                                x += 1
                                self.z = x*100/y
                                # time.sleep(1)
                                url = base_url[0].format(index)
                                yield scrapy.Request(url,
                                                cookies = {'api':'java'},
                                                headers = {'User-Agent':'PostmanRuntime'},
                                                callback = self.parse, errback = self.error_function)

        def parse(self, response):
                self.logger.info('------------------------------------------------{} %------------------------------------------------'.format(round(self.z, 2)))
                items = ResponseItem()
                allAds = response.css("ul.item2020 li.item")
                if hasattr(self, 'id'):                 #Muốn lấy danh sách id sản phẩm, truyền id bất kì vào terminal
                        for ad in allAds:
                                id_pro = ad.css("input::attr(value)").get()
                                items['link'] = id_pro
                                yield items
                else:                                   #Mặc định sẽ lấy danh sách URL
                        for ad in allAds:
                                link = ad.css("a::attr(href)").get()
                                items['link'] = self.domain+str(link)
                                yield items


        def error_function(self,failure):
                self.logger.info('------------------------------------------------{} %------------------------------------------------'.format(round(self.z, 2)))