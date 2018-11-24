# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import json
import random

class Image_Generator:

    dir_instance = ""

    start_x_pos = 3
    start_y_pos = 3
    # set position of letters

    rgb_tuple = (255, 255, 255)


    def __init__(self, dir_instance):
        self.dir_instance = dir_instance

    def _string_joiner(self, string, font, font_size):

        temp_string = ""
        max_text_width = 0
        text_height = 0

        img_font_instance = ImageFont.truetype(self.dir_instance.get_font_dir() + "/" + font, font_size)

        img_instance = Image.new("RGB", (10, 10), (255, 255, 255))
        temp_draw_instance = ImageDraw.Draw(img_instance)


        text_size = temp_draw_instance.multiline_textsize(text = string, font=img_font_instance)
        text_height += text_size[1]

        if max_text_width < text_size[0]:
            max_text_width = text_size[0]

        # set image width and height temporary
        # max_text_width = 100 * 3 - 15
        text_height = 48 -  15

        return (string, (max_text_width, text_height))

    def _list_checker(self, dict_list, label_list):
        for dict in dict_list:
            for ch in dict["text"]:
                if label_list.count(ch) == 0:
                    label_list.append(ch)

        return label_list


    def generator(self, font_size, data_list, mode):

        if mode == "word":
            save_dir = self.dir_instance.get_word_dataset_path() + "/"
            label_file_name = self.dir_instance.get_word_dataset_path() + "/" + mode + "_desc.json"
        elif mode == "one_line_string" :
            save_dir = self.dir_instance.get_one_line_dataset_path() + "/"
            label_file_name = self.dir_instance.get_one_line_dataset_path() + "/" + mode + "_desc.json"


        if self.dir_instance.is_json_exists(mode):
            with open(label_file_name, "r", encoding='utf-8') as json_file:
                json_data = json.load(json_file)
        else:

            json_data = {
                "abc":[],
                "train": [],
                "test": []
            }

        temp_list = []
        num_of_font = len(self.dir_instance.get_font_list())
        data_length = len(data_list)

        train_length = int(data_length * 0.85)
	

        for data_count in range(data_length):
            font_index = random.randrange(num_of_font)

            font_type = ImageFont.truetype(self.dir_instance.get_font_dir() + "/" + self.dir_instance.get_font_list()[font_index], font_size)
            print("\n" + str(data_count + 1) + " image generating...")
            string_tuple = self._string_joiner(data_list[data_count], self.dir_instance.get_font_list()[font_index], font_size)
            # (width, height) tuple: string_tuple[image_count][1]

            image_width = string_tuple[1][0] + 15
            image_height = string_tuple[1][1] + 15

            image_frame = Image.new("RGB", (image_width, image_height), self.rgb_tuple)
            generated_img = ImageDraw.Draw(image_frame)
            img_text = string_tuple[0]
            generated_img.multiline_text((self.start_x_pos, self.start_y_pos), img_text, font=font_type, fill='black')

            img_name = str(data_count + 1) + ".jpeg"

            temp_dict = {}
            temp_dict['text'] = string_tuple[0]
            temp_dict['name'] = img_name
            temp_list.append(temp_dict)

            if (data_count == train_length-1 or data_count == data_length-1):
                if len(json_data["train"]) < train_length:
                    json_data["train"].extend(temp_list)
                elif len(json_data["test"]) < data_length:
                    json_data["test"].extend(temp_list)

                json_data["abc"] = self._list_checker(temp_list, json_data["abc"])

                with open(label_file_name, "w", encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, indent=4, ensure_ascii=False)

                temp_list = []

            image_frame.save(open(save_dir + "/" + img_name, "wb"), "JPEG")
            print("complete!!... \n")
                       
            

    def multi_line_img_generator_15(self, string_list, user_input):

        font_size = 15
        img_name_list = []

        for font_count in range(len(self.dir_instance.get_font_list())):

            font_type = ImageFont.truetype(self.dir_instance.get_font_dir() + "/" + self.dir_instance.get_font_list()[font_count], self.font_size)
            string_tuple = self._string_joiner(string_list, self.dir_instance.get_font_list()[font_count])


            for image_count in range(len(string_tuple)):
                # (width, height) tuple: string_tuple[image_count][1]
                image_width = string_tuple[image_count][1][0] + 20
                image_height = string_tuple[image_count][1][1] - self.font_size * 10

                image_frame = Image.new("RGB", (image_width, image_height), self.rgb_tuple)
                generated_img = ImageDraw.Draw(image_frame)
                img_text = string_tuple[image_count][0]
                generated_img.multiline_text((self.start_x_pos, self.start_y_pos), img_text, font=font_type, fill='black')


                img_name = self.dir_instance.get_font_list()[font_count] + "_" + user_input + "_generated_" + str(image_count + 1) + ".jpeg"
                temp_dict = {}
                temp_dict['text'] = img_text
                temp_dict['name'] = img_name

                img_name_list.append(temp_dict)

                save_dir = self.dir_instance.get_save_dir_list()[font_count] + "/" + img_name
                image_frame.save(open(save_dir, "wb"), "JPEG")


        return img_name_list


    # convert dictionary to json and save
