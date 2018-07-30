# -*- coding: utf-8 -*-

'''

    Developed by DeepBIO Team, Handong Global University

    Text to Multi-line Image Data Generator (used NAVER OPEN API)

    March, 27, 2018

'''

import json
import random
import time

from os import getcwd
from sys import path
path.append(getcwd())

import dir_module
import crawler_module
import image_generator

def multi_line_img_generator():

        default_dir = "./data"

        dir_instance = dir_module.Dir_Module(default_dir)
        crawler_instance = crawler_module.Crawler_Module()
        generator_instance = image_generator.Image_Generator(dir_instance)

        user_input = ""
        repetition_count = 0
        repetition_numb = 0
        font_size = 0

        json_data = {
                "train": [],
                "test": []
        }

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
                crawled_result = crawler_instance.crawler()

                if crawled_result != -1:
                    print("     complete..!")



                    print("\n" + step + "th image generating..")
                    dict_results = generator_instance.img_generator_10(crawled_result, user_input)

#                    if dir_instance.is_json_exists():
#                        with open(dir_instance.get_json_file_path(), "r", encoding='utf-8') as json_file:
#                            json_data = json.load(json_file)
#                    else:
                    '''                        json_data = {
                            "train": [],
                            "test": []
                        }
                        
                    # for belbes CRNN
                    '''

                    if(len(json_data["train"]) <= 70000):
                        json_data["train"].extend(dict_results)
                    else:
                        json_data["test"].extend(dict_results)

                    print("     complete..!")

                    user_input = crawler_instance.find_less_crawled_element(crawled_result)

                   # with open(dir_instance.get_json_file_path(), "w", encoding='utf-8') as json_file:
                   #     json.dump(json_data, json_file, indent=4, ensure_ascii=False)

                else:
                    print("     Terminated..")
                    break
                with open(dir_instance.get_json_file_path(), "w", encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

            else:
                break

            time.sleep(random.randrange(1, 10))
            # for avoiding ip deny

            repetition_count += 1
