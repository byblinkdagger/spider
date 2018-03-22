import os
import time
import requests
from urllib import request
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

'''
米米小说专用
'''

baseurl = 'http://mimixiaoshuo.xyz'
url = 'http://mimixiaoshuo.xyz/home/search'


class MiMiBook(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS('C:\\Users\\Administrator\\pykit\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')  # Run in Windows need set executable_path.
        self.driver.maximize_window()
        print('webdriver start init success!')

    def __del__(self):
        try:
            self.driver.close()
            self.driver.quit()
            print('webdriver close and quit success!')
        except:
            pass

    # def _auto_scroll_to_bottom(self):
    #     '''
    #     将当前页面滑动到最底端
    #     '''
    #     js = "var q=document.body.scrollTop=10000"
    #     self.driver.execute_script(js)
    #     time.sleep(6)

    def getBookList(self,name):
        data = {
            'action': 'search',
            'q': name
        }

        response = requests.post(url=url, data=data)
        if response.status_code == requests.codes.ok:
            if url == response.url:
                # 多篇小说
                bs = BeautifulSoup(response.text, 'lxml')
                divs = bs.find_all(id='hotcontent')
                list = divs[1].find_all(attrs={'class': 'item-cover'})
                self.chooseBook(list)
            else:
                # 单篇小说
                print('仅找到一篇相关小说')
                self.parseBook(response.url)
        else:
            print('出错了' + str(response.status_code))

    def chooseBook(self,list):
        print('搜索到以下' + str(len(list)) + '本书：')
        for i in range(len(list)):
            print(str(i + 1) + ' ' + list[i].a.h3.get_text())
        num = int(input('请选择您需要的序号：'))
        self.parseBook(baseurl + list[num - 1].a['href'])

    def parseBook(self,url):
        resp = requests.get(url)
        bs = BeautifulSoup(resp.text, 'lxml')
        title = bs.find(class_='booktitle cf').h1.get_text()
        div = bs.find(id='list')
        num = len(div.dl.find_all(name='dd', recursive=False))
        print('共找到' + str(num) + '章')
        self.startDownload(url, num, title)

    def startDownload(self,url, num, title):

        dir = 'mytxt/'
        if not os.path.exists(dir):
            os.mkdir(dir)

        file = dir + title + '.txt'

        for i in range(num):
            durl = url + '/' + str(i) + '.html'

            self.driver.get(durl)

            try:
                print('正在下载第' + str(i + 1) + '章/共' + str(num) + '章')
                self.driver.implicitly_wait(20)
                wait = WebDriverWait(self.driver, 10)
                input = wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#content'), ' '))
                html = self.driver.page_source
                html2 = html.replace('<br /><br />', '\n')
                bs = BeautifulSoup(html2, 'lxml')
                t = bs.select('#wrapper > div.content_read > div > div.bookname > h1')[0].get_text()
                txt = bs.find(id='content').get_text()
                with open(file, 'a+', encoding='utf-8') as f:
                    f.write(t + '\n\n')
                    f.write(txt + '\n\n')
            except TimeoutException:
                print('无效章节')
                continue
        f.close()
        print('下载完成')

if __name__ == '__main__':
    name = input('请输入书名：')
    MiMiBook().getBookList(str(name))
