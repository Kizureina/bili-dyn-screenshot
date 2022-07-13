from flask import Flask, redirect, request
from selenium import webdriver
import time
from PIL import Image
from selenium.webdriver.chrome.options import Options
import requests,base64,lxml.html,json
from requests_toolbelt import MultipartEncoder

app = Flask(__name__)
@app.route('/api/bili_dyn_scnshot', methods=['POST','GET'])

def index():
    if request.method == 'POST':
        url = str('https://t.bilibili.com/' + request.form['dynid'])
        dyn_scnshot(url)
        imgurl = upload_to_JD("/mnt/e/apied.png")
        return imgurl

    if request.method == 'GET':
        return redirect("https://space.bilibili.com/1437582453")

def dyn_scnshot(url):
    chrome_options = Options()
    #chrome_options.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')
    chrome_options.add_argument('--lang=zh-CN')
    chrome_options.add_argument('window-size=1920x2500')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')
    chrome_driver = '/mnt/e/workplace/chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver,chrome_options=chrome_options)
    
    driver.maximize_window()
    driver.get(url)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    driver.execute_script('window.scrollTo(0, 0)')
    time.sleep(1)
    driver.get_screenshot_as_file("/mnt/e/api.png")
    #定位元素
    driver.implicitly_wait(10)

    pic_ele = driver.find_element("xpath", '//*[@id="app"]/div/div[2]/div/div/div/div[1]')
    left = pic_ele.location.get('x') - 120
    top = pic_ele.location.get('y') 
    right = pic_ele.size.get('width') + left + 160
    bottom = pic_ele.size.get('height') + top
    
    img = Image.open(r'/mnt/e/api.png')
    pic_ele = img.crop((left,top,right,bottom))
    pic_ele.save(r'/mnt/e/apied.png')
    driver.quit()


def img_to_base64(imagefile):
    image_data = open(imagefile, 'rb').read()
    return base64.b64encode(image_data)


def upload_to_JD(imagefile):
    url = 'https://imio.jd.com/uploadfile/file/post.do'
    headers = {
        'authority': 'imio.jd.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'dnt': '1',
        'accept': 'application/json',
        'origin': 'chrome-extension://dckaeinoeaogebmhijpkpmacifmpgmcb',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'cookie': 'shshshfpa=8ea1094b-9fa8-de6c-6074-c9106dd7607e-1628380635; shshshfpb=z%2FPs6TIxZfdRxtWgmXeif2g%3D%3D; pinId=PPaUOCiikPQ; pin=sirliu; unick=%E7%89%9B%E6%AD%A3%E6%96%87; _tp=7sn2a8%2F1SK1ezvQshrlpwg%3D%3D; _pst=sirliu; unpl=V2_ZzNtbUtfQEVwAU8Hfh4JVWIAEFhLAERGIlxEVS8cCABgA0ZZclRCFnUUR11nGlUUZwIZXEVcRhRFCENkexhdBWMGEV5EVnMlMEsWBi8FXABnBhtVQlJDF30JRl1yGV4AYh8RXUNVQxZ2CEdQeB5sBmczE21CUEAcdwFHU3kcXAdhAxNcRlVBEXUKR2RLGVQBVwMTXENXShFwC0RSeCmKq%2fPWmuKb5%2bbD36aT2cvM1a6zvZRtQl5DF30JR1R8GmwEVwIiHywUF0UoVBKC1reLvMdOElpBXkEcdA9EUXsbWgVmAhZfQFNDF3Q4R2R4; user-key=bb2545ac-0191-4acf-9722-1b93bf6d1836; cn=63; TrackID=1TxuaKNhgxgBtcr2M21qCh6VWbsfy37XyB2W4cljNpXutoeNlbHkYwaOI-2jc2FD6B5Lnak-gbw7hmta-HO2pCIFGysyaVDRBQ6DajTr3PUY; __jda=76161171.16283806341371005335130.1628380634.1630168669.1630859122.7; retina=1; cid=9; webp=1; visitkey=58375295313190738; TrackerID=HOOxXvvO80cvQXiVumgSsXxCj5j4FStKK8lWVeIjTVNmgGVxyt2APEwM-nX3lvq64dxnev681-bN0t6DBjIwyFoHmoP-LYVTCNujsg3v3m_4LV7zx1eqesUw1hfku-V4; pt_key=AAJhNPAPADBER43E6xvtQAb6JGiydrhu7yJll-q-Etg8Z4NoYH9pHk3sKTSMjW50txLw9Dyy3u0; pt_pin=sirliu; pt_token=l2rl7kn8; pwdt_id=sirliu; __wga=1630859280444.1630859280444.1630859280444.1630859280444.1.1; sc_width=400; shshshfp=5a972470188b5209659db1111a4ca4fa; mobilev=html5; cluster=1_file-dd.jd.local_file-dd.jd.local',
    }

    form_data = {
    'appId': 'im.customer',
    'aid': 'undefined',
    'clientType': 'comet',
    'pin': 'undefined',
    's': img_to_base64(imagefile)
    }

    # 生成可用于 multipart/form-data 上传的数据
    m = MultipartEncoder(form_data)
    # 自动生成 Content-Type 类型和随机码
    headers['Content-Type'] = m.content_type

    # 使用 data 上传文件
    r = requests.post(url, headers=headers, data=m)
    json_strs = lxml.html.document_fromstring(r.text).find('body').text
    try:
        json_obj = json.loads(json_strs)
        if json_obj['desc'] == "上传成功":
            print(json_obj['path'])
            return json_obj['path']
        else:
            print(imagefile,json_obj)
    except Exception as e:
        print('遇到错误:',e,'图片文件：','')

