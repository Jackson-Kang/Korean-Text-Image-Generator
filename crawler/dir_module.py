import os, stat

class Dir_Module:

    dirname = ''
    generated_img_dir = ''
    font_dir = ''
    save_dir = ''

    def __init__(self, dirname):

        self.dirname = dirname
        self.generated_img_dir = self.dirname + '/generated_img_data'
        self.font_dir = self.dirname + '/fonts'
        
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
            print ('Error: Creating directory. ' + dirname)
        # create a directory
        
    def get_font_list(self):
        font_list = []
        fontnames = os.listdir(self.font_dir)
        
        return fontnames
        # get a list of all files contained in current path

    def get_font_dir(self):
        return self.font_dir

    def get_generated_img_dir(self):
        return self.generated_img_dir

    def get_save_dir(self):
        return self.save_dir

    def set_save_dir(self, dirname):
        self.save_dir = dirname

    # user-defined accessor

1
