# -*- coding: utf-8 -*-

'''

    Developed by DeepBIO Team, Handong Global University

    Text to Image Data Generator (used NAVER OPEN API)

    March, 27, 2018

'''

from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

import dir_module
import crawler_module
import image_generator


if __name__ == "__main__":

    default_dir = "./data"

    dir_instance = dir_module.Dir_Module(default_dir)
    crawler_instance = crawler_module.Crawler_Module()
    generator_instance = image_generator.Image_Generator(dir_instance)

    user_input = ""
    repetition_count = 0
    repetition_numb = 0
    font_size = 0

    while True:

        if repetition_count == 0:
            user_input =  str(input("검색어 입력\n     Press Q or q to quit     : "))

            if user_input == "Q" or user_input == "q":
                break

            repetition_numb = int(input("반복 횟수 입력: "))
            font_size = int(input("font 크기는? : "))


        if repetition_count != repetition_numb:

            crawler_instance.set_user_input(user_input)
            dir_instance.set_user_input(user_input)
            generator_instance.set_font_size(font_size)

            dir_instance.create_image_subdir(user_input)

            step = str(repetition_count + 1)

            print("\n" + step + "th crawling..")
            crawled_list = crawler_instance.crawler()
            user_input = crawler_instance.find_less_crawled_element(crawled_list)
            print(user_input)
            print("     complete..!")

            print("\n" + step + "image generating..")
            generator_instance.img_generator_10(crawled_list, user_input)
            print("     complete..!")
            print("\n")

        else:
            break

        repetition_count += 1