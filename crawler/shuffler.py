import random
import json

''' 
        This src is for shuffling data which recorded in desc.json

        Developed by Jackson, Kang from DeepBIO project team.
         
        June, 27, 2018

'''


if __name__ == "__main__":

    print("\nShuffling...\n")

    data = {}

    desc_json_path = '/home/goodday1478/data/img_data/generated_img_data/data/desc.json'

    with open(desc_json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    random.shuffle(data["train"])
    random.shuffle(data["test"])

    with open(desc_json_path, 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


    print("\nComplete..!!\n")