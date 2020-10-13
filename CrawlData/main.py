import os
import json
import pyautogui
import time

pyautogui.FAILSAFE = True

def Calculator(x, y, length):
        if x % y == 0:
                return length
        return length + 1

def Empty(path):
        #xóa nội dung file cũ
        if os.path.exists(path):
                f = open(path, 'w', encoding = 'utf8')
                f.close()

def DeleteFile(path_import):
        i = 0
        while os.path.exists(path_import.format(i)):
                os.remove(path_import.format(i))
                i += 1

def ExportFile(path_Parent, path_import, max_col):                                                
        if os.path.exists(path_Parent):                                         # Kiểm tra file có tồn tại không
                if os.stat(path_Parent).st_size != 0:                           # Kiểm tra file có nội dung không
                        data = json.load(open(path_Parent, 'r'))                # Đọc json
                        length = len(data)//max_col                             # Mặc định sẽ chia nhỏ file thành các file nhỏ có kích thước tối đa là max_col dòng

                        leng = Calculator(len(data), max_col, length)           # Tính toán số file sẽ được chia nhỏ
                        
                        x = 0
                        y = max_col        
                        for i in range(leng):
                                f = open((path_import.format(i)), 'w')          # Lệnh mở file và gán thành f
                                json.dump(data[x:y], f, indent = 1)             # Lấy dữ liệu từ vị trí x --> y trong file data gán vào f
                                x += max_col
                                y += max_col
                        f.close()
                else:
                        print('File data is Empty')
        else:
                print('File does not exist')

def ExportFileForCate():
        cates = {42, 0, 44, 54, 55, 56, 57, 58, 60, 75, 85, 86, 522, 1262, 1363, 1662, 1882, 1902, 2162, 3885, 4727, 4728, 5693, 5697,
                5698, 6858, 6859, 6862, 7077, 7264, 7922, 7923, 7924, 7925, 9041}
        flag = 0
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        for i in cates:
                flag += 1
                pyautogui.typewrite('scrapy crawl TGDD -o output/cate_{id}.json -a cate={cate} -a id=1'.format(id = i, cate = i), interval = 0.01)
                time.sleep(1)
                pyautogui.hotkey('enter')
                time.sleep(1)
                if flag <= 2:
                        pyautogui.hotkey('ctrl', 'shift', '5')
                        time.sleep(1)
                else:
                        flag = 0
                        pyautogui.hotkey('ctrl', 'shift', '`')
                        time.sleep(1)

#Crawl data sản phẩm
def AutoRun(path_import, check):

        i = 0
        while os.path.exists(path_import.format(i)):                            #Lấy số lượng các file đã được chia nhỏ
                i += 1

        if i > 0:
                flag = 0
                pyautogui.hotkey('ctrl', 'shift', '`')
                time.sleep(1)
                for m in range(i):
                        flag += 1
                        pyautogui.typewrite('scrapy crawl {name} -a para={para}'.format(para = m, name = 'linkProTgdd' if check else 'linkProDmx'), interval = 0.01)
                        time.sleep(1)
                        pyautogui.hotkey('enter')
                        time.sleep(1)
                        if flag <= 2:
                                pyautogui.hotkey('ctrl', 'shift', '5')
                                time.sleep(1)
                        else:
                                flag = 0
                                pyautogui.hotkey('ctrl', 'shift', '`')
                                time.sleep(1)   
        else:
                print('File does not exist')

#AutoRun Cart 2 site
def AutoRun2Site(max_col):

        DeleteFile('./output/output_id_{}.json')
        DeleteFile('./output/output_id_dmx_{}.json')

        ExportFile('output_id.json', './output/output_id_{}.json', max_col)
        ExportFile('output_id_dmx.json', './output/output_id_dmx_{}.json', max_col)

        tgdd = 0
        while os.path.exists('./output/output_id_{}.json'.format(tgdd)):
                tgdd += 1

        dmx = 0
        while os.path.exists('./output/output_id_dmx_{}.json'.format(dmx)):
                dmx += 1

        length = tgdd
        if dmx > tgdd:
                length = dmx
                
        flag = 0
        check = True
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        for m in range(length):
                if m < tgdd:
                        flag += 1
                        pyautogui.typewrite('scrapy crawl tgdd -a id={}'.format(m), interval = 0.01)
                        time.sleep(1)
                        pyautogui.hotkey('enter')
                        time.sleep(1)
                        if flag <= (5 if check else 2):
                                pyautogui.hotkey('ctrl', 'shift', '5')
                                time.sleep(1)
                        else:
                                flag = 0
                                pyautogui.hotkey('ctrl', 'shift', '`')
                                time.sleep(1)
                else: check = False

                if m < dmx:
                        flag += 1
                        pyautogui.typewrite('scrapy crawl dmx -a id={}'.format(m), interval = 0.01)
                        time.sleep(1)
                        pyautogui.hotkey('enter')
                        time.sleep(1)
                        if flag <= (5 if check else 2):
                                pyautogui.hotkey('ctrl', 'shift', '5')
                                time.sleep(1)
                        else:
                                flag = 0
                                pyautogui.hotkey('ctrl', 'shift', '`')
                                time.sleep(1)
                else: check = False

#Crawl data cart
def AutoRun_Cart(path_import):

        i = 0
        while os.path.exists(path_import.format(i)):
                i += 1

        if i > 0:                                        # Kiểm tra file có tồn tại không
                flag = 0
                pyautogui.hotkey('ctrl', 'shift', '`')
                time.sleep(1)
                for m in range(i):
                        flag += 1
                        pyautogui.typewrite('scrapy crawl tgdd -a id={}'.format(m), interval = 0.01)
                        time.sleep(1)
                        pyautogui.hotkey('enter')
                        time.sleep(1)
                        if flag <= 2:
                                pyautogui.hotkey('ctrl', 'shift', '5')
                                time.sleep(1)
                        else:
                                flag = 0
                                pyautogui.hotkey('ctrl', 'shift', '`')
                                time.sleep(1)
        else:
                print('File does not exist')

class Run():
        # ExportFileForCate()
        path = os.getcwd().replace('\\','/')
        max_col = 1000                                                          # Số dòng tối đa của file được chia nhỏ 
        site1 = 'TGDD'
        site2 = 'DMX'
        site3 = 'AutoRun 2 site'
        option = pyautogui.confirm('Path = ' + path + '\nPlease choose options', buttons = [site1, site2, site3])

        if option ==  site3:
                col = pyautogui.prompt('Enter max_col. Default max_col = {}'.format(max_col))
                if col == '':
                        col = max_col
                else:
                        if int(col) <= 0:
                                print('Please enter max_col > 0')
                                exit()
                AutoRun2Site(int(col))
        exit() if option != site1 and option != site2 else True

        option1 = 'Crawl with LINK Product'
        option2 = 'Crawl with ID Product'
        option3 = 'AutoRun'
        option4 = 'Delete File'
        
        options = pyautogui.confirm('Path = '+ path + '\nEnter option \n', buttons = [option1, option2])

        if options == option1:
                option1_1 = 'Export File Link'
                option1_2 = 'Export File from File Link'
                path_Parent = 'output_link.json' if option == site1 else 'output_link_dmx.json'
                path_import = './output/output_link_{}.json' if option == site1 else './output/output_link_dmx_{}.json'
                option1s = pyautogui.confirm('Path = '+ path +'\nEnter option \n', buttons = [option1_1, option1_2, option3, option4])
                        
                if option1s == option1_1:
                        # Xóa nội dung file
                        Empty(path_Parent)
                        # Lệnh chạy scrapy và xuất kết quả ra file json
                        os.system('scrapy crawl TGDD -o output_link.json') if option == site1 else os.system('scrapy crawl DMX -o output_link_dmx.json')
                else:
                        if option1s == option1_2:
                                col = pyautogui.prompt('Enter max_col. Default max_col = {}'.format(max_col))
                                if col == '':
                                        col = max_col
                                ExportFile(path_Parent, path_import, int(col))
                        else:
                                if option1s == option3:
                                        AutoRun(path_import, True if option == site1 else False)
                                else:
                                        if option1s == option4:
                                                DeleteFile(path_import)
        else:
                if options == option2:
                        option2_1 = 'Export File Id'
                        option2_2 = 'Export File from File Id'
                        path_Parent = 'output_id.json' if option == site1 else 'output_id_dmx.json'
                        path_import = './output/output_id_{}.json' if option == site1 else './output/output_id_dmx_{}.json'
                        option2s = pyautogui.confirm('Path = ' + path + '\nEnter option \n', buttons = [option2_1, option2_2, option3, option4])

                        if option2s == option2_1:
                                # Xóa nội dung file
                                Empty(path_Parent)
                                # Lệnh chạy scrapy và xuất kết quả ra file json
                                os.system('scrapy crawl TGDD -o output_id.json -a id=1') if option == site1 else os.system('scrapy crawl DMX -o output_id_dmx.json -a id=1')
                        else:
                                if option2s == option2_2:
                                        col = pyautogui.prompt('Enter max_col. Default max_col = {}'.format(max_col))
                                        if col == '':
                                                col = max_col
                                        ExportFile(path_Parent, path_import, int(col))
                                else:
                                        if option2s == option3:
                                                AutoRun_Cart(path_import)
                                        else:
                                                if option2s == option4:
                                                        DeleteFile(path_import)
