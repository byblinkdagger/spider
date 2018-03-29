import requests
import os

def get_meizhi(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    if (r.status_code == requests.codes.ok):
        gank_data = r.json()
        result = gank_data['results']
        # print(result[0]['url'])
        img = result[0]['url']
        #download
        root = "E://love//"
        path = root +img.split("/")[-1]
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                pic = requests.get(img)
                pic.raise_for_status()
                # 使用with语句可以不用自己手动关闭已经打开的文件流
                with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(pic.content)
                print("爬取完成")
            else:
                print("文件已存在")
        except Exception as e:
            print("爬取失败:" + str(e))

if __name__ == '__main__':
    url ='http://gank.io/api/random/data/福利/1'
    while 1:
        get_meizhi(url)
