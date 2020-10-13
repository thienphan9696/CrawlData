# -*- coding: utf-8 -*-
import scrapy
import urllib
import cookies
import os
import time
import re

from scrapy.http import Request

class ResponseItem(scrapy.Item):
    link = scrapy.Field()
    # id_pro= scrapy.Field()

class ProductDMX(scrapy.Spider):
        start_time = time.time()
        name = 'DMX'      
        Cate = 0                        # 0: All
                                        # 1: CategoryV3
                                        # 2: CategoryV2
                                        # 3: TeleCommunication
                                        # 4: AccessoriesV3
        flag = False
        if Cate == 0:
            flag = True
        key = False
        z = 0
        x = 0
        y = 0

        domain = 'https://www.dienmayxanh.com'

        param_CategoryV3 = 'aj/CategoryV3/ProductBox'

        param_CategoryV2 = 'aj/CategoryV2/ProductBox'

        param_TeleCommunication = 'aj/TeleCommunication/ProductBox'

        param_AccessoriesV3 = 'aj/AccessoriesV3/ListProductCate'

        #Truyền tham số
        
        payload = 'catid={catid}&pagesize=20&pageidx={pageidx}&sortby=1&ishasfeatures=-1'
        payload_AccessoriesV3 ='CategoryId={catid}&Size=20&Index={pageidx}'
        CategoryV3= {1942, 2162, 1943, 166, 1944, 2202, 3385, 1962, 1922, 2222, 1989, 2064, 1988, 1983, 1982, 8984, 8979, 9138, 5612, 2342, 5554, 8967,
                    3305, 1987, 2063, 1986, 1985, 2062, 2262, 5473, 7498, 1992, 5541, 7720, 4706, 8121, 8858, 8860, 8861, 8862, 8980, 7278, 7419, 9000,
                    1990, 4697, 7859, 1991, 4645, 1984, 5475, 7604, 4366, 7358, 346, 8878, 5105, 7685, 8762, 9055, 365, 366, 8968, 9099, 324,
                    8620, 7902, 8621, 8890, 8898, 8899, 8901, 8923, 2322, 7684, 7173, 7901, 7899, 9058}
        CategoryV2= {5205, 2403, 2402, 4927, 4930, 4928, 4929, 5229, 8560, 3187, 7940, 4946, 5225, 5231, 8060,
                    5228, 5226, 5230, 7481, 3736, 7479, 3729, 8765}
        TeleCommunication = {42, 44, 522, 5698, 5697, 5693, 7264}
        AccessoriesV3 = {57, 58, 54, 2162, 55, 75, 1902, 99999, 86, 5452, 5005, 2824, 2825, 4727, 4728, 9118, 9119,
                        60, 1662, 1363, 7922, 7923, 6859, 56, 7924, 3885, 6882, 7925, 6858, 1882, 85}

        def start_requests(self):
            payload_finals_CategoryV3 = []
            payload_finals_CategoryV2 = []
            payload_finals_TeleCommunication = []
            payload_finals_AccessoriesV3 = []
            _urls = '{domain}/{param}'
            def Switch_CategoryV3(x):           #Tivi, máy lạnh, máy giặt, ...
                switcher= { 1942:11,            #tivi
                            2162:2,             #loa karaoke
                            1943:10,            #tủ lạnh
                            166:2,              #tủ đông
                            1944:10,            #máy giặt
                            2202:1,             #máy sấy quần áo
                            3385:4,             #máy lọc nước
                            1962:7,             #máy nước nóng
                    #đồ điện gia dụng
                            1922:9,             #nồi cơm điện
                            2222:2,             #cây nước nóng lạnh
                            # 2063:2,             #nồi chiên không dầu
                            1989:4,             #bình đun siêu tốc
                            2064:1,             #bình thủy điện
                            1988:4,             #bàn ủi
                            1983:3,             #bếp gas
                            1982:4,             #bếp từ
                            3305:2,             #bếp hồng ngoại
                            1987:3,             #lò vi sóng
                            2063:4,             #lò nướng
                            1986:1,             #lẩu điện
                            1985:5,             #máy xay sinh tố
                            2062:2,             #máy ép trái cây
                            2262:1,             #máy đánh trứng
                            5473:2,             #máy lọc không khí
                            7498:3,             #quạt điều hòa
                            1992:4,             #quạt
                            1990:3,             #máy hút bụi
                            4697:7,             #dụng cụ sửa chữa
                            7859:1,             #Thiết bị chăm sóc sức khoẻ
                            1991:3,             #Máy sấy tóc
                            4645:1,             #máy hút mùi
                            1984:2,             #nồi áp suất
                            5475:1,             #máy rửa chén
                            7604:2,             #Máy bơm, rửa xe, ổn áp
                            4366:1,             #vợt bắt muỗi
                            7358:1,             #Bóng đèn led
                            346:1,              #ổ cắm, phích cắm
                            8878:1,             #Miếng lót thấm sữa
                            5105:2,             #Phụ kiện máy lọc nước
                            7685:1,             #Máy hút chân không
                            8762:1,             #Nắp bồn cầu
                            5541:4,             #Vali kéo
                            7720:1,             #Máy mài, cắt, cưa
                            4706:1,             #Bộ dụng cụ đa năng
                            8121:1,             #Thang nhôm
                            8858:1,             #Mũi khoan
                            8860:1,             #Kìm
                            8861:1,             #Cờ lê - Mỏ lết
                            8862:1,             #Tua vít
                            8980:1,             #Ổ khóa
                            8984:1,             #Thước đo, cân cầm tay
                            8979:1,             #Búa
                            9138:1,             #Máy hàn
                            5612:1,             #Máy rửa xe
                            366:1,              #Nhiệt kế
                            365:1,              #Máy đo huyết áp    
                            8968:1,             #Máy khí dung
                            9099:1,             #Máy tăm nước
                            2342:1,             #Máy tạo kiểu tóc
                            5554:1,             #Máy cạo râu
                            7278:1,             #Máy wax lông
                            7419:1,             #Máy tỉa lông mũi
                            324:1,              #Máy massage
                            8967:1,             #Máy rửa mặt
                            9000:1,             #Máy phun sương
                            8620:1,             #Máy tiệt trùng bình sữa
                            7902:1,             #Máy hâm sữa
                            8621:1,             #Máy hút sữa
                            8890:1,             #Cốc, túi trữ sữa
                            8898:1,             #Bình sữa
                            8899:1,             #Núm ti
                            8901:1,             #Ti giả
                            8923:1,             #Núm trợ ti
                            2322:1,             #Máy làm sữa hạt
                            7684:1,             #Máy pha cà phê
                            7173:1,             #Máy làm tỏi đen
                            7901:1,             #Máy sấy trái cây
                            7899:1,             #Hộp hâm cơm
                            9058:1             #Phụ kiện nồi chiên không dầu
                }
                return switcher.get(x,-1)
            def Switch_CategoryV2(x):           #Đồ dùng gia đình
                switcher= { 5205:5,             #Bình, ly giữ nhiệt
                            2403:8,             #Chảo
                            2402:13,            #Nồi
                            4927:2,             #Bộ lau nhà
                            4930:3,             #Bình đựng nước
                            4928:14,            #Chén Bát
                            4929:4,             #Hộp đựng thực phẩm
                            5229:2,             #Hũ đựng thực phẩm
                            8560:4,             #Phụ kiện nhà bếp
                            3187:2,             #Dao, kéo, thớt
                            7940:2,             #Vệ sinh nhà cửa
                            4946:1,             #Khay đá - ly làm đá
                            5225:1,             #Bình, Ly
                            5231:2,             #Thau, rổ, gáo nước
                            8060:1,             #Phụ kiện máy giặt
                            5228:1,             #Thùng đá, ca đá
                            5226:1,             #Muỗng, đũa
                            5230:4,             #Vá, sạn
                            7481:1,             #Dụng cụ kẹp gắp
                            3736:1,             #Dụng cụ làm bánh
                            7479:1,             #Vỉ - thùng nướng
                            3729:2,             #Móc kẹp quần áo
                            8765:2,             #Mũ bảo hiểm
                            9055:1             #Ổn áp
                }
                return switcher.get(x,-1)
            def Switch_TeleCommunication(x):            #Điện thoại di động các kiểu
                switcher= { 42:9,                       #Điện thoại di động
                            44:11,                      #Laptop
                            522:2,                      #Tablet
                            5698:1,                     #Máy tính để bàn
                            5697:1,                     #Màn hình máy tính
                            5693:1,                     #Máy in
                            7264:91                    #Đồng hồ thời trang 
                }
                return switcher.get(x,-1)
            def Switch_AccessoriesV3(x):                #Phụ kiện các kiểu
                switcher= { 57:4,                       #Pin sạc dự phòng
                            58:12,                      #Sạc, cáp
                            54:7,                       #Tai nghe
                            2162:7,                     #Loa
                            55:1,                       #Thẻ nhớ
                            75:1,                       #USB
                            1902:1,                     #Ổ cứng di động
                            99999:10,                    #Phụ kiện chính hãng
                            86:2,                       #Chuột máy tính
                            5452:1,                     #Điều khiển tivi
                            5005:1,                     #Khung treo tivi
                            2824:2,                     #Cáp HDMI, cáp tivi
                            2825:1,                     #Giá đỡ máy giặt
                            4727:2,                     #Thiết bị mạng
                            4728:1,                     #Camera hành trình
                            9041:1,                     #Phụ kiện oto
                            9118:1,                     #Android TV Box
                            9119:1,                     #Bút trình chiếu
                            60:99,                     #Ốp lưng điện thoại
                            1662:1,                     #Ốp lưng tablet
                            1363:13,                    #Miếng dán màn hình
                            7922:1,                     #Quạt mini
                            7923:2,                     #Balo, túi chống sốc
                            6859:1,                     #Túi chống nước
                            56:2,                       #Pin
                            7924:2,                     #Đế, móc điện thoại
                            3885:1,                     #Gậy tự sướng
                            6882:1,                     #Gía đỡ Đt
                            7925:2,                     #Túi đựng airpods
                            6858:1,                     #Miếng lót bàn phím
                            1882:1,                     #Phụ kiện thông minh
                            85:1                       #Phần mềm
                }
                return switcher.get(x,-1)
            
            if (True if self.flag else self.Cate == 1):
                for ct in self.CategoryV3:
                    self.y+=Switch_CategoryV3(ct)
            if (True if self.flag else self.Cate == 2):
                for ct in self.CategoryV2:
                    self.y+=Switch_CategoryV2(ct)
            if (True if self.flag else self.Cate == 3):
                for ct in self.TeleCommunication:
                    self.y+=Switch_TeleCommunication(ct)
            if (True if self.flag else self.Cate == 4):
                for ct in self.AccessoriesV3:
                    self.y+=Switch_AccessoriesV3(ct)

            if (True if self.flag else self.Cate == 1):
                for cate1 in self.CategoryV3:
                    for i in range(Switch_CategoryV3(cate1)):
                        payload_finals_CategoryV3.append(self.payload.format(catid = cate1, pageidx = i))
                for payload1 in payload_finals_CategoryV3:
                    self.x += 1
                    self.z = self.x*100/self.y
                    self.begin_request_time= time.time()
                    url = _urls.format(domain = self.domain, param = self.param_CategoryV3)
                    yield scrapy.Request(url, method= 'POST', body = payload1,
                                            # cookies = {'api':'java'},
                                            headers = {'Content-Type': 'application/x-www-form-urlencoded'},
                                            callback = self.parse)

            if (True if self.flag else self.Cate == 2):
                for cate2 in self.CategoryV2:
                    for i in range(Switch_CategoryV2(cate2)):
                        payload_finals_CategoryV2.append(self.payload.format(catid = cate2, pageidx = i))
                for payload2 in payload_finals_CategoryV2:
                    self.x += 1
                    self.z = self.x*100/self.y
                    self.begin_request_time= time.time()
                    url = _urls.format(domain = self.domain, param = self.param_CategoryV2)
                    yield scrapy.Request(url, method = 'POST', body = payload2,
                                            # cookies = {'api':'java'},
                                            headers = {'Content-Type': 'application/x-www-form-urlencoded'},
                                            callback = self.parse)

            if (True if self.flag else self.Cate == 3):
                for cate3 in self.TeleCommunication:
                    for i in range(Switch_TeleCommunication(cate3)):
                        payload_finals_TeleCommunication.append(self.payload.format(catid = cate3, pageidx = i))
                for payload3 in payload_finals_TeleCommunication:
                    self.x += 1
                    self.z = self.x*100/self.y
                    self.begin_request_time= time.time()
                    url = _urls.format(domain = self.domain, param = self.param_TeleCommunication)
                    yield scrapy.Request(url, method = 'POST', body = payload3,
                                            # cookies = {'api':'java'},
                                            headers = {'Content-Type': 'application/x-www-form-urlencoded'},
                                            callback = self.parse)
            
            if (True if self.flag else self.Cate == 4):
                self.key = True
                for cate4 in self.AccessoriesV3:
                    for i in range(Switch_AccessoriesV3(cate4)):
                        payload_finals_AccessoriesV3.append(self.payload_AccessoriesV3.format(catid=cate4, pageidx=i))
                for payload4 in payload_finals_AccessoriesV3:
                    self.x += 1
                    self.z = self.x*100/self.y
                    self.begin_request_time= time.time()  
                    url = _urls.format(domain = self.domain, param = self.param_AccessoriesV3)
                    yield scrapy.Request(url, method= 'POST', body = payload4,
                                            # cookies = {'api':'java'},
                                            headers = {'Content-Type': 'application/x-www-form-urlencoded'},
                                            callback = self.parse)

        def parse(self, response):
            _time = time.time()-self.start_time
            current_time= time.time()- self.begin_request_time
            if _time > 60:
                time1 = int(_time//60)
                time2 = int(_time%60)
                self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time1}p{time2}s'.format(percent = round(self.z, 2), current_time=round(current_time, 2),time1=time1, time2=time2))
            else:
                self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time}s'.format(percent = round(self.z, 2),current_time=round(current_time, 2),time = round(time.time()-self.start_time,2)))
                
            items = ResponseItem()
            allAds = response.css("li")
            if hasattr(self, 'id'):         #Muốn lấy danh sách id sản phẩm, truyền id bất kì vào terminal
                if self.key:
                    for ad in allAds:                            
                        id_pro = ad.css("div.label-pos img::attr(src)").get()
                        if len(re.findall(r'\d+', str(id_pro))) > 0:
                            items['link'] = re.findall(r'\d+', str(id_pro))[1]
                            yield items
                else:
                    for ad in allAds:
                        id_pro = ad.css("a::attr(data-pid)").get()
                        items['link'] = id_pro
                        yield items
            else:                           #Mặc định sẽ lấy danh sách URL
                for ad in allAds: 
                    link = ad.css("a::attr(href)").get()
                    items['link'] = self.domain + str(link) 
                    yield items

        def error_function(self,failure):
            _time = time.time()-self.start_time
            current_time= time.time()- self.begin_request_time
            if _time > 60:
                time1 = int(_time//60)
                time2 = int(_time%60)
                self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time1}p{time2}s'.format(percent = round(self.z, 2), current_time=round(current_time, 2),time1=time1, time2=time2))
            else:
                self.logger.info('progress: {percent} % ---Current time: {current_time}s--- time: {time}s'.format(percent = round(self.z, 2),current_time=round(current_time, 2),time = round(time.time()-self.start_time,2)))