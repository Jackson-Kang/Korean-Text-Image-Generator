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
    hgu1_file_path = ""
    char_dataset_path = ""
    multi_line_dataset_path=""
    one_line_dataset_path=""
    word_dataset_path = ""

    char_image_save_path = ""

    def __init__(self, dirname):

        self.dirname = dirname
        self.generated_img_dir = self.dirname + '/generated_img_data'
        self.font_dir = self.dirname + '/fonts'
        self.hgu1_file_path = self.dirname + '/hgu1_files'
        self.HanDB_save_path = self.generated_img_dir + '/char_dataset'
        self.json_path = self.dirname + "/generated_img_data/desc.json"

        self.char_dataset_path = self.generated_img_dir + '/char_dataset'
        self.multi_line_dataset_path = self.generated_img_dir + '/multi_line_dataset'
        self.one_line_dataset_path = self.generated_img_dir + '/one_line_dataset'
        self.word_dataset_path = self.generated_img_dir + '/word_dataset'


        self._create_dir(self.dirname)
        self._create_dir(self.generated_img_dir)
        self._create_dir(self.font_dir)

        self._create_dir(self.char_dataset_path)
        self._create_dir(self.multi_line_dataset_path)
        self._create_dir(self.one_line_dataset_path)
        self._create_dir(self.word_dataset_path)

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

    def set_char_image_save_path(self, path):
        self.char_image_save_path = path

    def char_image_save_dir(self):
        return self.char_image_save_path

    def get_hgu1_file_path(self):
        return self.hgu1_file_path

    def get_hgu1_file_list(self, additional_path):
        return os.listdir(self.get_hgu1_file_path() + "/" + additional_path)

    def get_HanDB_save_path(self):
        return self.HanDB_save_path

    def is_json_exists(self, mode):
        json_filename = "/desc.json"
        if mode == "word":
            return os.path.isfile(self.word_dataset_path + json_filename)
        elif mode == "one_line":
            return os.path.isfile(self.one_line_dataset_path + json_filename)
        elif mode == "multi_line":
            return os.path.isfile(self.multi_line_dataset_path + json_filename)

    def get_word_dataset_path(self):
        return self.word_dataset_path

    def get_one_line_dataset_path(self) :
        return self.one_line_dataset_path
