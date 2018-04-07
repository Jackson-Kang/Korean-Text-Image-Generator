'''
    
    Developed by DeepBIO Team, Handong Global University

    Text to Image Data Generator (used NAVER OPEN API)

    March, 27, 2018
    
'''

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import random as rand

import dir_module


def crawler(numb):
    
    default = 'https://openapi.naver.com/v1/search/news.xml?'
    sort = 'sort-sim'
    start = '&start=1'
    display='&display=100'

    if numb == 1:
        query = '&query=' + urllib.parse.quote_plus(str(input("검색어 입력: ")))
    else:
        query = '&query=' + urllib.parse.quote_plus(str())

    fullURL = default + sort + start + display + query
    headers = {

        'Host': 'openapi.naver.com',
        'User-Agent': 'curl/7.43.0',
        'Accept' : '*/*',
        'Content-Type': 'application/xml',
        'X-Naver-Client-Id': '83KxnTRcS8MkfM701ekt',
        'X-Naver-Client-Secret': 'Hifv0wG6Yu'
    }
    req = urllib.request.Request(fullURL, headers = headers)
    html_code = urllib.request.urlopen(req)
    # request to API Server
    
    result_XML = html_code.read()
    parsed_XML = BeautifulSoup(result_XML, 'html.parser')
    items = parsed_XML.find_all('item')
    result = ""

    for item in items:
        result += item.title.get_text(strip = True) + item.description.get_text(strip = True)
    # data parsing

    sliced_result = result.split()
    # form - list of words

    return sliced_result

    
def img_generator(sliced_results, font, save_dirname):

    print(save_dirname)
    
    for i in range(len(sliced_results)):
        font_size = 15
        img_width = 800
        img_height = 600
        # set image frame and font size

        x_pos = img_width/3
        y_pos = img_height/3
        # set position of letters

        img_frame = Image.new("RGB", (img_width, img_height),(255,255,255))
        generated_img = ImageDraw.Draw(img_frame)
        
        font_type = ImageFont.truetype(font, 40)
        generated_img.text((x_pos,y_pos), sliced_results[i], font=font_type, fill='black')
        img_frame.save(open(save_dirname + "/generated_" + str(i) + ".jpeg", "wb"), "JPEG")
        # img generator


########################### Main ##############################


if __name__ == "__main__":

    default_dir = "./data"
    dir_instance = dir_module.Dir_Module(default_dir)
    # dir_instance

    crawling_results = crawler(1)

    font_len = len(dir_instance.get_font_list())
    
    for i in range(font_len):
        dir_instance.set_save_dir(dir_instance.get_generated_img_dir()+ '/' + dir_instance.get_font_list()[i])
        print(dir_instance.get_save_dir())
        dir_instance._create_dir(dir_instance.get_save_dir())
        img_generator(crawling_results, dir_instance.get_font_dir() + '/' + dir_instance.get_font_list()[i], dir_instance.get_save_dir())
       
