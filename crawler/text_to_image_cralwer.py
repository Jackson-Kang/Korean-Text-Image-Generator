# -*- coding: utf-8 -*-

'''
    
    Developed by DeepBIO Team, Handong Global University

    Text to Image Data Generator (used NAVER OPEN API)

    March, 27, 2018
    
'''

# meta data 정보 작성
# crawler 분리 후 file i/o로 검색어에 대한 결과 저장
# document parser -> 크기에 따라 엔터 넣어주기 (휴리스틱?)

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import random as rand

import dir_module


def crawler(dir_instance):
    
    default = 'https://openapi.naver.com/v1/search/news.xml?'
    sort = 'sort-sim'
    start = '&start=1'
    display='&display=100'

    numb = 1

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
    xml_code = urllib.request.urlopen(req)
    # request to API Server
    
    result_XML = xml_code.read()
    parsed_XML = BeautifulSoup(result_XML, 'lxml-xml')
    items = parsed_XML.find_all('item')


    font_list_len = len(dir_instance.get_font_list())

    for i in range(font_list_len):
        dir_instance.set_save_dir(dir_instance.get_generated_img_dir()+ '/' + dir_instance.get_font_list()[i])
        dir_instance._create_dir(dir_instance.get_save_dir())

    for item in items:
        result = ""
        title = strip_tag(item.title.get_text(strip = True))
        description = strip_tag(item.description.get_text(strip = True))
        
        temp_list = []
        
        for char in description:
            temp_list.append(char)

            if len(temp_list) % 80 == 0:
                temp_list.append('\n')

        for char in temp_list:
            result = result + char

        result += title

        for i in range(len(dir_instance.get_font_list())):
            img_generator(result, dir_instance.get_font_dir() + '/' + dir_instance.get_font_list()[i], dir_instance.get_save_dir(), i)
   

        

    

    


# create string parser module
def strip_tag(target_string):
    target_string = tag_converter(target_string, "&quot;", "\"")
    target_string = tag_converter(target_string, "<b>", "")
    target_string = tag_converter(target_string, "</b>", "")

    return target_string    


def tag_converter(target_string, target_tag, converting_tag):
    # convert &quot; into " and erace <br> or </br>.
    temp_list = target_string.split(target_tag)
    result = converting_tag.join(temp_list)

    return result


def img_generator(string, font, save_dirname, index):
    print(string)

    font_size = 10
    img_width = 800
    img_height = 600
    # set image frame and font size

    x_pos = 10
    y_pos = 10
    # set position of letters
    
    rgb_tuple = (255,255, 255)

    img_frame = Image.new("RGB", (img_width, img_height),rgb_tuple)
    generated_img = ImageDraw.Draw(img_frame)

    print(font)        
    font_type = ImageFont.truetype(font, font_size)
    generated_img.text((x_pos,y_pos), string, font=font_type, fill='black')
    img_frame.save(open(save_dirname + "/generated_" + str(index + 1) + ".jpeg", "wb"), "JPEG")
    # img generator



########################### Main ##############################


if __name__ == "__main__":

    default_dir = "./data"
    dir_instance = dir_module.Dir_Module(default_dir)
    # dir_instance


    print("running crawler..\n")

    crawling_results = crawler(dir_instance)

        # data parsing

