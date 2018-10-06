import sys
sys.path.append(sys.path[0] + '/modules/')

import image_generator
import HGU1_Generator
import dir_module
import string_parser


if __name__ == "__main__":


    default_dir = "/mnt/ssd512/goodday1478/data"
    dir_instance = dir_module.Dir_Module(default_dir)

    

    image_generator_instance =image_generator.Image_Generator(dir_instance)

    print("initiating...")
    data = string_parser.json_file_loader()
    # parsed text using desc.json

    print("\n\n[Word] data generating...")
    word_list = data['word_list']
    image_generator_instance.generator(data_list=word_list, font_size=42, mode="word")


    print("\n\n[Sentence] data generating...")
    one_line_string_list = data["one_line_string_list"]
    image_generator_instance.generator(data_list=one_line_string_list, font_size=42, mode="one_line_string")



