# -*- coding: utf-8 -*-

import os


class Dir_Module:
    dirname = ''
    generated_img_dir = ''
    generated_img_dir_list = []
    font_dir = ''
    save_dir = ''
    user_input = ""
    json_path = ""

    def __init__(self, dirname):

        self.dirname = dirname
        self.generated_img_dir = self.dirname + '/generated_img_data'
        self.font_dir = self.dirname + '/fonts'
        self.generated_img_dir_list = []

        self.json_path = "./data/generated_img_data/desc.json"

        self._create_dir(self.dirname)
        self._create_dir(self.generated_img_dir)
        self._create_dir(self.font_dir)

        for root, dirs, files in os.walk(self.dirname):
            for directory in dirs:
                os.chmod(root + '/' + directory, 0o755)
        # create dir structure

    def _create_dir(self, dirname):
        try:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
        except OSError:
            print('Error: Creating directory. ' + dirname)
        # create a directory

    def create_image_subdir(self, user_input):

        self.user_input = user_input
        self.generated_img_dir_list = []

        font_list_len = len(self.get_font_list())
        for i in range(font_list_len):
            self.set_save_dir(self.get_generated_img_dir() + '/' + self.get_font_list()[i])
            self.generated_img_dir_list.append(self.get_save_dir())
            self._create_dir(self.get_save_dir())
        # create save_dir

    def get_font_list(self):
        fontnames = os.listdir(self.font_dir)

        return fontnames
        # get a list of all files contained in current path

    def get_font_dir(self):
        return self.font_dir

    def get_generated_img_dir(self):
        return self.generated_img_dir

    def get_save_dir(self):
        return self.save_dir

    def get_save_dir_list(self):
        return self.generated_img_dir_list

    def get_json_file_path(self):
        return self.json_path

    def set_user_input(self, user_input):
        self.user_input = user_input

    def set_save_dir(self, dirname):
        self.save_dir = dirname
        # user-defined accessor

    def is_json_exists(self):
        return os.path.isfile(self.json_path)
