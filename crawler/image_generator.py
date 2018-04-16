# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont

class Image_Generator:

    dir_instance = ""
    font_size  = 15

    def __init__(self, dir_instance):
        self.dir_instance = dir_instance

    def _string_joiner(self, string_list, font):

        temp_string = ""
        max_text_tuple = []
        max_text_width = 0
        text_height = 0
        count = 1

        img_font_instance = ImageFont.truetype(self.dir_instance.get_font_dir() + "/" + font, self.font_size)

        img_instance = Image.new("RGB", (10, 10), (255, 255, 255))
        temp_draw_instance = ImageDraw.Draw(img_instance)

        for string in string_list:
            temp_string += string
            text_size = temp_draw_instance.multiline_textsize(text = string, font=img_font_instance)
            text_height += text_size[1]

            if max_text_width < text_size[0]:
                max_text_width = text_size[0]

            if count%10 == 0:
                max_text_tuple.append((temp_string, (max_text_width, text_height)))
                max_text_width = 0
                temp_string = ""
                text_height = 0
                count = 0

            count = count + 1

        return max_text_tuple

    def set_font_size(self, font_size):
        self.font_size = font_size

    def img_generator_10(self, string_list, user_input):

        start_x_pos = 10
        start_y_pos = 10
        # set position of letters

        rgb_tuple = (255, 255, 255)

        for font_count in range(len(self.dir_instance.get_font_list())):

            font_type = ImageFont.truetype(self.dir_instance.get_font_dir() + "/" + self.dir_instance.get_font_list()[font_count], self.font_size)
            string_tuple = self._string_joiner(string_list, self.dir_instance.get_font_list()[font_count])

            for image_count in range(len(string_tuple)):
                # (width, height) tuple: string_tuple[image_count][1]
                image_width = string_tuple[image_count][1][0] + 20
                image_height = string_tuple[image_count][1][1] - self.font_size * 12

                image_frame = Image.new("RGB", (image_width, image_height), rgb_tuple)
                generated_img = ImageDraw.Draw(image_frame)
                generated_img.multiline_text((start_x_pos, start_y_pos), string_tuple[image_count][0], font=font_type, fill='black')

                save_dir = self.dir_instance.get_save_dir_list()[font_count] + "/" + user_input + "_generated_" + str(image_count + 1) + ".jpeg"
                image_frame.save(open(save_dir, "wb"), "JPEG")

