from PIL import Image
import base64

def hgu1_image_generator(dir_instance):

    count = 0

    HGU1_file_list = dir_instance.get_hgu1_file_list("HanDB_train")

    for hgu_file in HGU1_file_list:
        break
        # error: image read write

        with open(dir_instance.get_hgu1_file_path() + "/HanDB_train/" + hgu_file, "rb") as input_file:
            pass

        '''
        
        file_header = input_file.read(8)

        # Read and create Image files.

        while True:
            # read code & check EoF
            code = input_file.read(2)

            if len(code) < 2:
                break
            # Create New file
            output_file =  open(dir_instance.get_HanDB_save_path() + "/" + str(count) + ".jpeg", "wb")
            # Write class id and code of image

            class_id = count.to_bytes(2, 'big')
            output_file.write(class_id)
            output_file.write(code)

            width = input_file.read(1)
            output_file.write(width)

            height = input_file.read(1)
            
            output_file.write(height)

            reserved = input_file.read(2)

            image_bytes = input_file.read(width[0] * height[0])
            output_file.write(image_bytes)
            # class_id(2bytes)+code(2bytes)+width(1byte)+height(1byte)+image_bytes(64)
            output_file.close()
            count += 1

        input_file.close()
        '''