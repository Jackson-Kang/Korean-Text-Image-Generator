import random
import json


if __name__ == "__main__":

    print("\nShuffling...\n")

    data = {}

    desc_json_path = '/home/goodday1478/data/img_data/generated_img_data/data/desc.json'

    with open(desc_json_path, encoding="utf-8") as json_file:
        data = json.load(json_file)

    random.shuffle(data["train"])
    random.shuffle(data["test"])

    with open(desc_json_path, 'w') as outfile:
        json.dump(data, outfile)


    print("\nComplete..!!\n")